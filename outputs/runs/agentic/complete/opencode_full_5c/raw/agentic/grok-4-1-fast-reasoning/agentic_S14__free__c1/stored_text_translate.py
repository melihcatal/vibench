from google.cloud import translate_v2 as translate
from storage_client import get_storage_client


def translate_stored_text(
    bucket: str, object_key: str, target_language: str = "en"
) -> str:
    s3_client = get_storage_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text_content = response["Body"].read().decode("utf-8")
    translate_client = translate.Client()
    result = translate_client.translate(text_content, target_language=target_language)
    return result["translatedText"]
