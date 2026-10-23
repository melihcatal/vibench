import boto3
from storage_client import get_s3_client


def stored_text_translate(
    bucket_name: str,
    object_name: str,
    source_language: str = "en",
    target_language: str = "es",
) -> dict:
    s3_client = get_s3_client(region="us-east-1")
    obj_response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    text = obj_response["Body"].read().decode("utf-8")
    translate_client = boto3.client("translate", region_name="us-east-1")
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response
