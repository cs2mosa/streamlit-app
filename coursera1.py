from moviepy.editor import AudioFileClip
from pytubefix import YouTube
import assemblyai
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from openai import OpenAI

def get_wav(audio_dir):
    audio_clip = AudioFileClip(audio_dir)
    file_name = f"{audio_dir}.wav"
    audio_params = {
        "codec": "pcm_s16le",
        "fps": 16000, # Set the desired sampling rate: 16000 Hz
        # "fps": 8000, # Alternatively, set the sampling rate to 8000 Hz
        "nchannels": 2, # Mono audio
        "bitrate": "16k" # Set the desired bitrate
    }
    audio_clip.write_audiofile(file_name, codec=audio_params["codec"],fps=audio_params["fps"],nbytes=2,bitrate=audio_params["bitrate"])
    return file_name

def get_audio(link):
    lecture = YouTube(link)
    audio = lecture.streams.filter(only_audio=True, file_extension='mp4').first()
    answer =  audio.download()
    return answer


model_size = "large-v3"
model = WhisperModel(model_size)
#now we go with the speech recognizing shit
def get_text_small(file_name):
    result,_ = model.transcribe(file_name,beam_size=5, language="ar", condition_on_previous_text=False)
    result = list(result)
    whole_text = ""
    for resul in result:
        whole_text+= resul.text

    with open ("transcription.txt","w") as f:
        f.write(whole_text)


def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 1000 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 1000,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=300,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = get_text_small(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(text)
            whole_text += text
    # return the text for all chunks detected
    return whole_text
