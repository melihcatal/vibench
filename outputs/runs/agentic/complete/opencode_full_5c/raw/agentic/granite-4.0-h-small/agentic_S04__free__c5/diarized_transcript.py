import os
import json
import requests

# provider: Google Cloud Speech-to-Text
API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
BASE_URL = "https://speech.googleapis.com/v1/speech:recognize"


def diarized_transcript(audio_path, speaker_count=2):
    """
    Request speaker diarization for a batch audio file.
    Returns a transcript with speaker labels.
    """
    with open(audio_path, "rb") as f:
        audio_content = f.read()
    payload = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "en-US",
            "diarizationConfig": {
                "enableSpeakerDiarization": True,
                "minSpeakerCount": speaker_count,
                "maxSpeakerCount": speaker_count,
            },
            "enableAutomaticPunctuation": True,
        },
        "audio": {"content": audio_content.decode("latin1")},
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    # Convert alternative[0] text and word_time_offsets
    transcript = result["results"][0]["alternatives"][0]["transcript"]
    words = result["results"][0]["alternatives"][0]["words"]
    with_speakers = []
    for w in words:
        word = w["word"]
        start = w["startTime"]
        end = w["endTime"]
        diarization = w.get("speakerTag")
        with_speakers.append(f"Speaker {diarization}: {word} ({start}->{end})")
    return "\\n".join(with_speakers)
