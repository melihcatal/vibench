from typing import Dict, List, Union

class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

def normalize_translation_response(response: Dict[str, Union[str, List[Dict[str, str]]]]) -> List[TranslationResponse]:
    normalized_responses = []
    for item in response.get('TranslatedTexts', []):
        normalized_responses.append(TranslationResponse(
            translated_text=item['TranslatedText'],
            source_language=item['SourceLanguageCode'],
            target_language=item['TargetLanguageCode']
        ))
    return normalized_responses