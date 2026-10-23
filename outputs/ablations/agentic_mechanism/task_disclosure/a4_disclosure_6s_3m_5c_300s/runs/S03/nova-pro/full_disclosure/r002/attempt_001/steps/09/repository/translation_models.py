from typing import Dict, List, Any

import boto3


class TranslationRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Text': self.text,
            'SourceLanguageCode': self.source_language_code,
            'TargetLanguageCode': self.target_language_code
        }


class TranslationResponse:
    def __init__(self, translated_text: str, source_language_code: str, target_language_code: str):
        self.translated_text = translated_text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranslationResponse':
        return cls(
            translated_text=data['TranslatedText'],
            source_language_code=data['SourceLanguageCode'],
            target_language_code=data['TargetLanguageCode']
        )


def normalize_text(text: str) -> str:
    # Simple normalization: remove extra spaces and newlines
    return ' '.join(text.split())


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = boto3.client('translate')
    response = client.translate_text(**request.to_dict())
    return TranslationResponse.from_dict(response)