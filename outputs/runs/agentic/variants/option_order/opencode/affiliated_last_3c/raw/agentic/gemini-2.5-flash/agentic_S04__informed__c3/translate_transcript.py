from speech_client import speech_client
from speech_models import TranslationRequest


def translate_transcript(request: TranslationRequest) -> str:
    response = speech_client.translate_client.translate_text(
        request={
            "parent": request.parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
        }
    )
    return response.translations[0].translated_text
