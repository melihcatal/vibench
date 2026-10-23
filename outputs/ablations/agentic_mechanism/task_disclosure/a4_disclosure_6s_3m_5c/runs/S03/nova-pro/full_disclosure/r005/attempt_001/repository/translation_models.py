from typing import Dict, List, Any


class TranslationRequest:
    def __init__(self, source_text: str, source_language: str, target_language: str):
        self.source_text = source_text
        self.source_language = source_language
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            'SourceText': self.source_text,
            'SourceLanguageCode': self.source_language,
            'TargetLanguageCode': self.target_language
        }


class TranslationResponse:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranslationResponse':
        return cls(
            translated_text=data['TranslatedText'],
            source_language=data['SourceLanguageCode'],
            target_language=data['TargetLanguageCode']
        )


def normalize_translation_response(response: Dict[str, Any]) -> TranslationResponse:
    return TranslationResponse.from_dict(response)


# Example usage with Amazon Translate
import boto3

def translate_text(source_text: str, source_language: str, target_language: str) -> TranslationResponse:
    client = boto3.client('translate')
    request = TranslationRequest(source_text, source_language, target_language)
    response = client.translate_text(**request.to_dict())
    return normalize_translation_response(response)