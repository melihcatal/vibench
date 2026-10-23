from speech_client import get_translation_client
from speech_models import TranslationRequest


def translate_script(request: TranslationRequest) -> str:
    client = get_translation_client()

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return result["translatedText"]
