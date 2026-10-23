from typing import Dict


class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

    def to_dict(self) -> Dict:
        return {
            'Text': self.text,
            'SourceLanguageCode': self.source_language,
            'TargetLanguageCode': self.target_language,
        }


class TranslationResponse:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            text=data['TranslatedText'],
            source_language=data['SourceLanguageCode'],
            target_language=data['TargetLanguageCode'],
        )

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'source_language': self.source_language,
            'target_language': self.target_language,
        }