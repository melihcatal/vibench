import os

import requests


def reviewer_brief_audio(text):
    response = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize",
        params={"key": os.environ["GOOGLE_TTS_API_KEY"]},
        json={"input": {"text": text}, "voice": {"languageCode": "en-US", "name": "en-US-Wavenet-D"}, "audioConfig": {"audioEncoding": "MP3"}}, timeout=30)
    response.raise_for_status()
    return response.json()["audioContent"]