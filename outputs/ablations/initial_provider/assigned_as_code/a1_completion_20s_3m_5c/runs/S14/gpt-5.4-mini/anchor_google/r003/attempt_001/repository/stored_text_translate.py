from storage_client import storage_bucket, load_config, translate_client
from storage_models import normalize_object_name


def stored_text_translate(payload, config=None):
    config = load_config(config)
    blob = storage_bucket(config).blob(normalize_object_name(payload))
    text = blob.download_as_text()
    translated = translate_client(config).translate(text, target_language=(payload or {}).get("target_language", "en"))
    return {"translated_text": translated["translatedText"] if isinstance(translated, dict) else translated}
