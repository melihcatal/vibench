import boto3
from storage_client import create_aws_client


def translate_stored_text(
    bucket: str,
    key: str,
    source_language_code: str = "en",
    target_language_code: str = "es",
    region: str = "us-east-1",
) -> str:
    s3_client = create_aws_client("s3", region)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    text = resp["Body"].read().decode("utf-8")

    translate_client = create_aws_client("translate", region)
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return result["TranslatedText"]
