import os
from google.cloud import translate_v2 as translate
from typing import Optional


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = translate.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    
    return result["translatedText"]