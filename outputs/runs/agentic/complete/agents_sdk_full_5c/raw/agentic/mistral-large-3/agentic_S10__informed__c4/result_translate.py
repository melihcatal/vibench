import os
from typing import Optional
from google.cloud import translate_v2 as translate


def translate_result(
    text: str,
    target_language: str = "es",
    model: Optional[str] = "nmt"
) -> str:
    """
    Translate generated model output using Google Cloud Translation.
    """
    client = translate.Client()
    
    result = client.translate(
        text,
        target_language=target_language,
        model=model
    )
    
    return result['translatedText']