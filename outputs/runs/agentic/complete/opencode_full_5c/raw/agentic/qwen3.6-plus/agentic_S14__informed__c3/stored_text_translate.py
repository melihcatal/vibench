import os
import deepl
from storage_client import get_oss_bucket, normalize_object_key


def translate_stored_text(
    bucket_name: str,
    object_key: str,
    target_language: str = "EN",
    source_language: str = None,
) -> dict:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    object_stream = bucket.get_object(object_key)
    document_bytes = object_stream.read()
    source_text = document_bytes.decode("utf-8", errors="replace")

    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)

    translate_options = {
        "target_lang": target_language,
    }
    if source_language:
        translate_options["source_lang"] = source_language

    result = translator.translate_text(source_text, **translate_options)

    return {
        "success": True,
        "object_key": object_key,
        "bucket": bucket_name,
        "source_language": result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_language,
        "target_language": target_language,
        "translated_text": result.text,
        "provider": "DeepL API",
    }
