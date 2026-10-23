import os
from google.cloud import translate_v2 as translate
from .identity_models import ConsentText


def translate_identity_consent(
    consent: ConsentText, target_language: str = "en"
) -> str:
    client = translate.Client()
    result = client.translate(
        consent.text,
        target_language=target_language,
        source_language=consent.source_language,
    )
    return result["translatedText"]
