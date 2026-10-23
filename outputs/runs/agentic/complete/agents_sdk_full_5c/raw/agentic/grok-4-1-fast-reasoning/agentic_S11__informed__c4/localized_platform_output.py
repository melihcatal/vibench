from google.cloud import translate_v2 as translate
from typing import Optional

def localize_platform_output(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None
) -> str:
    """
    Translate platform model output for another locale using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    return result["translatedText"]
