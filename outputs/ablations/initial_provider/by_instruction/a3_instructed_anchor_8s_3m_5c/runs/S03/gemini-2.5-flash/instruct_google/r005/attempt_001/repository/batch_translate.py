from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(requests: list[TranslationRequest]) -> list[TranslationResponse]:
    client = get_translate_client()
    parent = f"projects/{{YOUR_PROJECT_ID}}/locations/global"

    contents = [req.text for req in requests]
    target_language = requests[0].target_language # Assuming all requests have the same target language
    source_language = requests[0].source_language if requests[0].source_language else None # Assuming all requests have the same source language

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": contents,
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": contents,
                "target_language_code": target_language,
            }
        )

    translated_responses = []
    for translation in response.translations:
        translated_responses.append(TranslationResponse(translation.translated_text, translation.detected_language_code))

    return translated_responses
