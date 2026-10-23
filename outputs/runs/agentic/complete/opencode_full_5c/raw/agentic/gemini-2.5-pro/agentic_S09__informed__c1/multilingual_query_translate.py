import os
import deepl
from typing import Optional


def translate_query(
    query: str, source_lang: Optional[str] = None, target_lang: str = "EN-US"
) -> str:
    """
    Translates a query to a target language using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        query, source_lang=source_lang, target_lang=target_lang
    )

    return result.text


if __name__ == "__main__":
    # This is an example and will not be executed
    german_query = "Was ist die Hauptstadt von Deutschland?"
    translated_text = translate_query(german_query, source_lang="DE")
    print(f"Original: {german_query}")
    print(f"Translated: {translated_text}")

    spanish_query = "Dónde está la biblioteca?"
    translated_text_es = translate_query(spanish_query)  # Auto-detect source
    print(f"Original: {spanish_query}")
    print(f"Translated: {translated_text_es}")
