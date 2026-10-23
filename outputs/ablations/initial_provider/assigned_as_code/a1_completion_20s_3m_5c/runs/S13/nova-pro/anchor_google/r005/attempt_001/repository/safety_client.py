import os

import requests


class PerspectiveClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def analyze(self, text):
        response = requests.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            params={"key": self.api_key},
            json={"comment": {"text": text}, "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def translate(self, text, target_language):
        response = requests.post(
            "https://translation.googleapis.com/language/translate/v2",
            params={"key": self.api_key},
            data={"q": text, "target": target_language},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def embed(self, text):
        response = requests.post(
            "https://language.googleapis.com/v1/documents:analyzeEntities",
            params={"key": self.api_key},
            json={"document": {"type": "PLAIN_TEXT", "content": text}},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def generate_audio(self, text):
        response = requests.post(
            "https://texttospeech.googleapis.com/v1/text:synthesize",
            params={"key": self.api_key},
            json={"input": {"text": text}, "voice": {"languageCode": "en-US", "name": "en-US-Wavenet-D"},
                   "audioConfig": {"audioEncoding": "MP3"}},
            timeout=30
        )
        response.raise_for_status()
        return response.json()


def get_perspective_client(config=None):
    api_key = config.get('api_key') or os.environ.get('PERSPECTIVE_API_KEY')
    return PerspectiveClient(api_key)