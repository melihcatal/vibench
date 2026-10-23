# [LATER-STEP] record_translate.py

# Example using Google Cloud Translation for text translation
# Identifier: Service = Cloud Translation, SDK = google-cloud-translate

from google.cloud import translate_v2 as translate


def translate_field(record: dict, target_lang: str = "es") -> dict:
    """Translate a specific user-facing field in the record to a target language.

    The function assumes the document contains a key 'content' that holds the
    text to translate. It returns a new dictionary with an additional key
    '{field}_translated' containing the translated text.

    Args:
        record (dict): Document record from NoSQL store.
        target_lang (str): ISO language code for the target language (default 'es').

    Returns:
        dict: Updated record with translated field.
    """
    # Authenticate via GOOGLE_APPLICATION_CREDENTIALS environment variable
    translator = translate.Client()

    source_text = record.get("content", "")
    if not source_text:
        return record  # nothing to translate

    # Perform translation
    result = translator.translate(source_text, target_language=target_lang)
    translated_text = result["translatedText"]

    # Add translated version to record
    record["content_translated"] = translated_text
    return record
