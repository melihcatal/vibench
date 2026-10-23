import boto3
from storage_client import get_managed_storage_client

# Example translation provider: AWS Translate (managed translation service)


def translate_text_from_storage(
    bucket_name: str, object_key: str, target_lang: str = "es"
) -> dict:
    """Extract text from a stored document and translate it using managed translation service.

    Returns translation response from AWS Translate.
    """
    client = get_managed_storage_client()
    # Download stored document bytes
    obj = client.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = obj["Body"].read()

    # Use a simple text extraction helper (e.g., splitting lines for demo)
    text = document_bytes.decode("utf-8", errors="ignore")

    translate = boto3.client("translate", region_name=boto3.Session().region_name)
    translation = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_lang
    )
    return translation
