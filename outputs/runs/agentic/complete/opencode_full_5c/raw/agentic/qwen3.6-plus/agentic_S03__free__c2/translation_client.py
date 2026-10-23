import os
from typing import Optional
import deepl

DEEPL_API_ENDPOINT = "https://api.deepl.com/v2/translate"
DEEPL_FREE_API_ENDPOINT = "https://api-free.deepl.com/v2/translate"


def get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    api_key = auth_key or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    server_url = os.environ.get("DEEPL_SERVER_URL", DEEPL_API_ENDPOINT)
    return deepl.Translator(api_key, server_url=server_url)


def build_translation_options(
    source_lang: str = "EN",
    target_lang: str = "ES",
    preserve_formatting: bool = True,
    tag_handling: Optional[str] = None,
    formality: Optional[str] = None,
) -> dict:
    options = {
        "source_lang": source_lang.upper(),
        "target_lang": target_lang.upper(),
        "preserve_formatting": preserve_formatting,
    }
    if tag_handling:
        options["tag_handling"] = tag_handling
    if formality:
        options["formality"] = formality
    return options


def extract_translation_result(result) -> str:
    return result.text


def extract_batch_results(results) -> list:
    return [r.text for r in results]
