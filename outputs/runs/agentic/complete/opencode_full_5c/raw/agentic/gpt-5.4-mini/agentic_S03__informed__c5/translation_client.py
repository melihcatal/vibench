import os
from functools import lru_cache
from typing import Any, Dict, List, Optional

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from translation_models import (
    normalize_dict_values,
    normalize_text,
    normalize_text_list,
    split_markup_segments,
)


AZURE_TRANSLATOR_ENDPOINT = os.getenv(
    "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
)


@lru_cache(maxsize=1)
def get_translation_client() -> TextTranslationClient:
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    return TextTranslationClient(
        endpoint=AZURE_TRANSLATOR_ENDPOINT,
        credential=AzureKeyCredential(key),
        region=region,
    )


def translate_text_value(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    client = get_translation_client()
    result = client.translate(
        content=[normalize_text(text)],
        to=[target_language],
        from_parameter=source_language,
    )
    return result[0].translations[0].text


def translate_text_list(
    values: List[str], target_language: str, source_language: Optional[str] = None
) -> List[str]:
    client = get_translation_client()
    texts = normalize_text_list(values)
    if not texts:
        return []
    result = client.translate(
        content=texts, to=[target_language], from_parameter=source_language
    )
    return [item.translations[0].text for item in result]


def translate_markup_value(
    markup: str, target_language: str, source_language: Optional[str] = None
) -> str:
    segments = split_markup_segments(markup)
    texts = [segment["text"] for segment in segments if segment.get("type") == "text"]
    translations = translate_text_list(texts, target_language, source_language)
    translated_iter = iter(translations)
    rebuilt: List[str] = []
    for segment in segments:
        if segment.get("type") == "text":
            rebuilt.append(next(translated_iter))
        elif segment.get("type") == "start":
            attrs = "".join(f' {k}="{v}"' for k, v in segment.get("attrs", []))
            rebuilt.append(f"<{segment['tag']}{attrs}>")
        else:
            rebuilt.append(f"</{segment['tag']}>")
    return "".join(rebuilt)


def translate_dict_values(
    values: Dict[str, Any], target_language: str, source_language: Optional[str] = None
) -> Dict[str, str]:
    client = get_translation_client()
    normalized = normalize_dict_values(values)
    keys = list(normalized.keys())
    texts = [normalized[key] for key in keys]
    if not texts:
        return {}
    result = client.translate(
        content=texts, to=[target_language], from_parameter=source_language
    )
    return {key: result[index].translations[0].text for index, key in enumerate(keys)}
