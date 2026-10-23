import os
from typing import List, Dict
import alibabacloud_alimt
from storage_client import get_s3_client


def translate_extracted_text(
    bucket_name: str, object_key: str, target_language: str = "en"
) -> List[Dict]:
    """Translate text extracted from a stored document using Alibaba Cloud Machine Translation.

    Steps:
    1. Retrieve the document via S3 client from storage_client.get_s3_client().
    2. Decode content as UTF-8 plain text.
    3. Call Alibaba Cloud Translate API (aliyun SDK) with detected source language.
    """
    s3 = get_s3_client()
    metadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    if "ContentType" not in metadata or not metadata["ContentType"].startswith(
        "text/plain"
    ):
        raise ValueError("Object is not plain text suitable for translation")

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    plain_text = response["Body"].read().decode("utf-8")

    client = alibabacloud_alimt.AliyunClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    translate_response = client.translate(
        SourceText=plain_text,
        SourceLanguage="auto",
        TargetLanguage=target_language,
        Scenario="general",
    )

    translations = translate_response["Data"]["Translated"]
    return [
        {"source": plain_text, "target": translations[i]}
        for i in range(len(translations))
    ]
