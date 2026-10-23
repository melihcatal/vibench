from google.cloud import translate_v2 as translate
import os
from vision_models import AltTextTranslateRequest, AltTextTranslateResponse


def alt_text_translate(request: AltTextTranslateRequest) -> AltTextTranslateResponse:
    translate_client = translate.Client()
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected

    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    return AltTextTranslateResponse(translated_text=result["translatedText"])
