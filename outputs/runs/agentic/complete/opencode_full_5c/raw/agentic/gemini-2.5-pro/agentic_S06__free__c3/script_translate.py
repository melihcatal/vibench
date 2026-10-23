from google.cloud import translate_v2 as translate
from speech_models import TranslationRequest


def translate_script(request: TranslationRequest) -> str:
    """Translates text into the target language."""
    translate_client = translate.Client()

    result = translate_client.translate(
        request.script_content,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return result["translatedText"]
