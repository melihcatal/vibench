from google.cloud import storage
from google.cloud import translate_v2 as translate

from storage_client import get_bucket
from storage_models import DocumentInsight, normalize_object_name


def stored_text_translate(bucket_name: str, object_name: str, target_language: str = "en") -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    text = blob.download_as_text()
    client = translate.Client()
    translated = client.translate(text, target_language=target_language)
    return DocumentInsight(bucket=bucket_name, name=blob.name, text=text, translated_text=translated.get("translatedText"), language=translated.get("detectedSourceLanguage")).to_dict()
