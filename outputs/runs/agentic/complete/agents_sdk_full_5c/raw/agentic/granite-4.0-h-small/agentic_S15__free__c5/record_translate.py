from google.cloud import translate_v2 as translate

def translate_field(record: dict, field: str, target_lang: str = "en") -> dict:
    """Translates a specific field in a document record to the target language.

    Uses Google Cloud Translation API (managed service). Provider identifiable by hostname
    translate.googleapis.com and import google.cloud.translate_v2.
    
    Args:
        record (dict): Original document record.
        field (str): Field name to translate.
        target_lang (str): Target language code (default 'en').
    Returns:
        dict: New record with translated field added as <field>_translated.
    """
    client = translate.Client()
    source_text = record.get(field, "")
    if not source_text:
        return record  # nothing to translate
    result = client.translate(source_text, target_language=target_lang)
    translated = result.get('translatedText', '')
    # Preserve original field and add translated version
    new_record = record.copy()
    new_record[f"{field}_translated"] = translated
    return new_record
