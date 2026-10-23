import os
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Mapping

import boto3

from translation_models import normalize_mapping_values, normalize_text, normalize_texts


def _aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def client():
    return boto3.client("translate", region_name=_aws_region())


def translate_text(text: Any, source_language: str, target_language: str) -> str:
    response = client().translate_text(
        Text=normalize_text(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response.get("TranslatedText", "")


def translate_texts(texts: Iterable[Any], source_language: str, target_language: str) -> List[str]:
    return [translate_text(text, source_language, target_language) for text in normalize_texts(list(texts))]


def translate_markup(text: Any, source_language: str, target_language: str) -> str:
    response = client().translate_text(
        Text=normalize_text(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        Settings={"Brevity": "ON"},
        TerminologyNames=[],
    )
    return response.get("TranslatedText", "")


def translate_dictionary_values(values: Mapping[str, Any], source_language: str, target_language: str) -> Dict[str, Any]:
    normalized = normalize_mapping_values(values)
    result: Dict[str, Any] = {}
    for key, value in normalized.items():
        if isinstance(value, str):
            result[key] = translate_text(value, source_language, target_language)
        else:
            result[key] = value
    return result
