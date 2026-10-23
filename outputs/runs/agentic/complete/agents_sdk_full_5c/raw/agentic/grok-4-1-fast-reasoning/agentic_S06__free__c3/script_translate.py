from google.cloud import translate_v2 as translate
from typing import Optional

def translate_script(
    script: str,
    target_language: str = "en",
    source_language: Optional[str] = None
) -> str:
    """Translate narration scripts before synthesis."""
    client = translate.Client()
    if source_language:
        result = client.translate(script, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(script, target_language=target_language)
    return result["translatedText"]
