from pytubefix import YouTube
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import assemblyai
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from faster_whisper import WhisperModel
#returs youtube audio title

def get_audio(link):
    lecture = YouTube(link)
    audio = lecture.streams.filter(only_audio=True, file_extension='mp4').first()
    answer =  audio.download()
    return answer

def get_wav(audio_dir):
    audio_clip = AudioFileClip(audio_dir)
    file_name = f"{audio_dir}.wav"
    audio_params = {
        "codec": "pcm_s16le",
        "fps": 16000, # Set the desired sampling rate: 16000 Hz
        # "fps": 8000, # Alternatively, set the sampling rate to 8000 Hz
        "nchannels": 1, # Mono audio
        "bitrate": "16k" # Set the desired bitrate
    }
    audio_clip.write_audiofile(file_name, codec=audio_params["codec"],fps=audio_params["fps"],nbytes=2,bitrate=audio_params["bitrate"])
    return file_name

#configurations of the speech model nano to recognize arabic
configurations = assemblyai.TranscriptionConfig(speech_model=assemblyai.SpeechModel.nano, language_code="ar")

#now we go with the speech recognizing shit
assemblyai.settings.api_key = "2382a5e71cc6422693a53a10d879995e"
#now we go with the speech recognizing shit
def get_text_small(file_name):
    transcription = assemblyai.Transcriber().transcribe(file_name,config=configurations)
    sentences = transcription.get_sentences()
    for sentence in sentences:
        return sentence.text

def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 2000,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=100,
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
        #recognize the chunk
        try:
            text = str(get_text_small(chunk_filename))
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            whole_text += text
    # return the text for all chunks detected
    return whole_text

link = input("dfgdg: ")
get_audio(link)