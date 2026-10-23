from typing import List, Dict


class TranslationRequest:
    def __init__(self, text: str, target_lang: str):
        self.text = text
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, text: str):
        self.text = text


def normalize_response(response: str) -> str:
    return response.strip()
