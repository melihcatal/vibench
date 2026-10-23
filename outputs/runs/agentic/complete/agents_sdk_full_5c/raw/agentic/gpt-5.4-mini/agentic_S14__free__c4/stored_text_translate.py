from __future__ import annotations

from google.cloud import translate_v3 as translate

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectRef, TextDocument

GOOGLE_TRANSLATE_MODEL = "google-cloud-translate-v3"


def stored_text_translate(key: str, target_language_code: str, source_language_code: str = "") -> TextDocument:
    s3 = get_s3_client()
    bucket = get_bucket_name()
    content = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", errors="replace")

    client = translate.TranslationServiceClient()
    parent = f"projects/{client.transport._credentials.project_id if getattr(client.transport, '_credentials', None) else os.getenv('GOOGLE_CLOUD_PROJECT', '')}/locations/global"
    response = client.translate_text(
        contents=[content],
        target_language_code=target_language_code,
        source_language_code=source_language_code or None,
        parent=parent,
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return TextDocument(source=ObjectRef(bucket=bucket, key=key), text=translated, language=target_language_code, provider=GOOGLE_TRANSLATE_MODEL)
