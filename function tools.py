import requests
import json
import re


def get_youtube_transcript(video_id):
    # Fetch the video page
    response = requests.get(f"https://www.youtube.com/watch?v={video_id}")

    if response.status_code != 200:
        return "Failed to fetch the video page."

    # Extract the ytInitialData JSON
    match = re.search(r"ytInitialData\s*=\s*({.*?});", response.text)
    if not match:
        return "Failed to find transcript data."

    data = json.loads(match.group(1))

    # Navigate through the JSON to find the transcript data
    try:
        transcript_data = \
        data['playerOverlays']['playerOverlayRenderer']['decoratedPlayerBarRenderer']['decoratedPlayerBarRenderer'][
            'playerBar']['multiMarkersPlayerBarRenderer']['markersMap'][0]['value']['tracks'][0]['captionTrack']
        base_url = transcript_data['baseUrl']
    except (KeyError, IndexError):
        return "Transcript not available for this video."

    # Fetch the actual transcript
    transcript_response = requests.get(base_url)
    if transcript_response.status_code != 200:
        return "Failed to fetch the transcript."

    # Parse the transcript
    transcript = []
    for line in transcript_response.text.split('\n'):
        if re.match(r'\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+', line):
            continue
        if line.strip():
            transcript.append(line.strip())

    return ' '.join(transcript)


# Example usage
video_id = "U2K-_i-fnek"
transcript = get_youtube_transcript(video_id)
print(transcript)