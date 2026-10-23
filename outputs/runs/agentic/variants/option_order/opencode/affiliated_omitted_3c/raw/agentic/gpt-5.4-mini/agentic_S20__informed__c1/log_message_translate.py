from typing import List

import boto3


def translate_messages(messages: List[str], target_language: str) -> List[str]:
    client = boto3.client("translate")
    translated = []
    for message in messages:
        result = client.translate_text(
            Text=message, SourceLanguageCode="auto", TargetLanguageCode=target_language
        )
        translated.append(result.get("TranslatedText", ""))
    return translated
