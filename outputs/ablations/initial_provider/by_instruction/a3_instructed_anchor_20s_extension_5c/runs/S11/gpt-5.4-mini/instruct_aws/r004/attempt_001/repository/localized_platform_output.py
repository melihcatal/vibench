from typing import Any, Dict

import boto3


def localized_platform_output(text: str, target_locale: str) -> Dict[str, Any]:
    client = boto3.client("translate", region_name="us-east-1")
    result = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_locale)
    return result
