import os
import deepl
from database_models import Document


def translate_record(record: Document, target_lang: str) -> Document:
    """
    Translates user-facing fields of a document using DeepL.

    Args:
        record: The document to translate.
        target_lang: The target language code (e.g., "FR", "ES").

    Returns:
        A new Document with translated content.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    translated_record = record.copy()

    content_to_translate = record.get("content")
    if content_to_translate:
        try:
            result = translator.translate_text(
                content_to_translate, target_lang=target_lang
            )
            translated_record["content"] = result.text
        except deepl.DeepLException as e:
            print(f"Could not translate document content: {e}")

    return translated_record
