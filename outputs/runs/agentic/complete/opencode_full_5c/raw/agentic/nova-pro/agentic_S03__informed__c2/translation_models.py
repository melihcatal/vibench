from typing import Dict, List


class TranslationRequest:
    def __init__(self, text: str, source_lang: str, target_lang: str):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


def normalize_response(response: Dict) -> str:
    return response["data"]["translated"]


def batch_normalize_response(responses: List[Dict]) -> List[str]:
    return [normalize_response(response) for response in responses]
