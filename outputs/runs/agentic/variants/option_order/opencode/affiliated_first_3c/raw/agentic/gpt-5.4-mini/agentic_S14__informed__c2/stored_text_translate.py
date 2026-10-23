from __future__ import annotations

import boto3


def stored_text_translate(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    aws_region: str | None = None,
) -> dict:
    client = boto3.client("translate", region_name=aws_region)
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response
