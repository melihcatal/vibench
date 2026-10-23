from typing import Dict, Any

from speech_client import get_translate_client
from speech_models import normalize_translation_result

def translate_transcript(text: str, source_language_code: str, target_language_code: str, config: Dict[str, Any] = None) -> str:
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return normalize_translation_result(response)
