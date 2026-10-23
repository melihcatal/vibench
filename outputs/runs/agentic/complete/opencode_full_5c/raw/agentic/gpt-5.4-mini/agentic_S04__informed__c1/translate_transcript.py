import os
from typing import List

import boto3


def translate_transcript(
    segments: List[str], target_language_code: str = "es"
) -> List[str]:
    client = boto3.client("translate")
    return [
        client.translate_text(
            Text=segment,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language_code,
        )["TranslatedText"]
        for segment in segments
    ]
