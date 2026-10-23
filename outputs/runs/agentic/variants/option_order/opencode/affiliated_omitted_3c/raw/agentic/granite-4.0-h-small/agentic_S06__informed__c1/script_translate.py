import os
from typing import Iterator
from google.cloud import translate_v2 as translate


def translate_script(text: str, target_lang: str = "es") -> str:
    """Translate a script using Google Cloud Translation.

    Args:
        text (str): The source narration script.
        target_lang (str): Target language code (default 'es').

    Returns:
        str: Translated script.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
    )
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]


def batch_translate(paths: list[str], target_lang: str = "es") -> Iterator[str]:
    """Translate multiple scripts from file paths, yielding results in order."""
    client = translate.Client()
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        translated = client.translate(content, target_language=target_lang)[
            "translatedText"
        ]
        yield translated
