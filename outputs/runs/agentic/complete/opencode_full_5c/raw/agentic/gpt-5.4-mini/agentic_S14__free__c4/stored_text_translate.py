from google.cloud import translate_v3 as translate

from storage_client import get_bucket_name, get_object_key, get_s3_client


def stored_text_translate(bucket=None, key=None, target_language_code="en"):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=get_bucket_name(bucket), Key=get_object_key(key))
    text = obj["Body"].read().decode("utf-8")
    client = translate.TranslationServiceClient()
    parent = client.common_location_path("project", "global")
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=parent,
    )
    return response.translations[0].translated_text if response.translations else ""
