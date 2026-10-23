import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORG_ID"))


def get_translation_model() -> str:
    return os.getenv("TRANSLATION_MODEL", "gpt-5.4-mini")


def build_translation_instruction(source_language: str | None, target_language: str, preserve_tags: bool = False) -> str:
    parts = ["Translate the text accurately."]
    if source_language:
        parts.append(f"Source language: {source_language}.")
    parts.append(f"Target language: {target_language}.")
    if preserve_tags:
        parts.append("Preserve markup tags, attributes, entities, and structure exactly.")
    parts.append("Return only the translated result.")
    return " ".join(parts)
