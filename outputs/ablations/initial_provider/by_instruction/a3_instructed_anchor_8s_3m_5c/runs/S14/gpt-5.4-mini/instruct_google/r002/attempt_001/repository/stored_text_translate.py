from google.cloud import translate_v3

from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest


def stored_text_translate(request: ObjectMetadataRequest, target_language_code: str = "en") -> dict:
    client = get_storage_client()
    text = client.bucket(request.bucket).blob(request.name).download_as_text()
    translate_client = translate_v3.TranslationServiceClient()
    parent = "projects/placeholder/locations/global"
    response = translate_client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=parent,
        mime_type="text/plain",
    )
    translations = [item.translated_text for item in response.translations]
    return {"bucket": request.bucket, "name": request.name, "translations": translations}
