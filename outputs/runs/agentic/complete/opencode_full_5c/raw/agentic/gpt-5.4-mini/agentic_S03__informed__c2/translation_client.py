import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class TranslationConfig:
    api_key: str
    endpoint: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


def load_translation_config() -> TranslationConfig:
    api_key = os.environ.get('AZURE_TRANSLATOR_KEY', '')
    region = os.environ.get('AZURE_TRANSLATOR_REGION', '')
    endpoint = os.environ.get('AZURE_TRANSLATOR_ENDPOINT', f'https://api.cognitive.microsofttranslator.com')
    return TranslationConfig(api_key=api_key, endpoint=endpoint, source_lang=None, target_lang=None)


class TranslationClient:
    def __init__(self, config: Optional[TranslationConfig] = None):
        self.config = config or load_translation_config()
        self.session = requests.Session()
        if self.config.api_key:
            self.session.headers.update({'Ocp-Apim-Subscription-Key': self.config.api_key})
        region = os.environ.get('AZURE_TRANSLATOR_REGION')
        if region:
            self.session.headers.update({'Ocp-Apim-Subscription-Region': region})
        self.session.headers.update({'Content-Type': 'application/json'})

    def post(self, path: str, params=None, json=None):
        return self.session.post(f'{self.config.endpoint}{path}', params=params, json=json, timeout=30)
