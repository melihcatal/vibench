import os
import boto3
from typing import Dict

def translate_dictionary_values(d: Dict[str, str], source_lang: str, target_lang: str) -> Dict[str, str]:
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    result = {}
    for k, v in d.items():
        resp = translate_client.translate_text(
            Text=v,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        result[k] = resp["TranslatedText"]
    return result
