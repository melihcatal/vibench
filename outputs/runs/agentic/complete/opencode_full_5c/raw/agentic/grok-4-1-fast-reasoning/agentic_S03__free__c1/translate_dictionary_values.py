import boto3
import os
from typing import Dict


def translate_dictionary_values(
    d: Dict[str, str], source_lang: str, target_lang: str
) -> Dict[str, str]:
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))
    result = {}
    for key, value in d.items():
        response = client.translate_text(
            Text=value, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        result[key] = response["TranslatedText"]
    return result
