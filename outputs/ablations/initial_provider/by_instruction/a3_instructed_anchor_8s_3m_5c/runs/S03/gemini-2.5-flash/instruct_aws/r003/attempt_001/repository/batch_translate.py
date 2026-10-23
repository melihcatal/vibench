from typing import List
from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(texts: List[str], source_language_code: str, target_language_code: str) -> List[TranslationResponse]:
    client = get_translate_client()
    translated_responses = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_responses.append(TranslationResponse(
            translated_text=response['TranslatedText'],
            source_language_code=response['SourceLanguageCode'],
            target_language_code=response['TargetLanguageCode']
        ))
    return translated_responses
