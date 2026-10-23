import os
from google.cloud import translate_v2 as translate
from storage_client import ManagedObjectStorageClient


def translate_stored_text(bucket: str, key: str, target_language: str = "es") -> dict:
    """Translate text extracted from a stored document via Google Cloud Translation.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path to the text file (UTF-8).
        target_language (str): ISO language code (default "es").

    Returns:
        dict: Translation response with translated text and source language.
    """
    # Retrieve the source text file from S3
    s3 = ManagedObjectStorageClient(
        service="Amazon S3",
        credentials={
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    client_s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    obj = client_s3.get_object(Bucket=bucket, Key=key)
    source_text = obj["Body"].read().decode("utf-8")

    # Translate using Google Cloud Translation API
    client = translate.Client()
    result = client.translate(source_text, target_language=target_language)
    return {
        "translatedText": result["translatedText"],
        "sourceLanguage": result["src"],
        "detectedSourceLanguage": result.get("detectedSourceLanguage"),
    }
