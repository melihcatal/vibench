from typing import Dict

import boto3


def alt_text_translate(text: str, target_language_code: str) -> Dict[str, str]:
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"provider": "aws.translate", "translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode", "")}
