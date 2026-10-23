from typing import Dict, List, Union

import boto3


class TranslationRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

    def to_dict(self) -> Dict[str, Union[str, List[str]]]:
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

    @staticmethod
    def from_dict(response: Dict[str, Union[str, List[str]]]) -> 'TranslationResponse':
        return TranslationResponse(
            translated_text=response['TranslatedText'],
            source_language_code=response['SourceLanguageCode'],
            target_language_code=response['TargetLanguageCode']
        )


def normalize_translation_response(response: Dict[str, Union[str, List[str]]]) -> str:
    return response['TranslatedText']


def send_translation_request(request: TranslationRequest) -> TranslationResponse:
    client = boto3.client('translate')
    response = client.translate_text(**request.to_dict())
    return TranslationResponse.from_dict(response)