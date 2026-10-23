import os

import requests


def reviewer_brief_audio(text, config=None):
    client_id = config.get("client_id") or os.environ["GOOGLE_CLOUD_TEXT_TO_SPEECH_CLIENT_ID"]
    client_secret = config.get("client_secret") or os.environ["GOOGLE_CLOUD_TEXT_TO_SPEECH_CLIENT_SECRET"]
    response = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize",
        params={"input": {"text": text}, "voice": {"languageCode": "en-US", "name": "en-US-Wavenet-D"},
                "audioConfig": {"audioEncoding": "MP3"}},
        auth=(client_id, client_secret), timeout=30)
    response.raise_for_status()
    return response.json()["audioContent"]