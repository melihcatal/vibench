import os
import boto3
from typing import AsyncGenerator, Dict, Any


def translate_live_captions(
    text_stream: AsyncGenerator[str, None],
    source_lang: str = "en",
    target_lang: str = "es",
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Translates live captions into another language using Amazon Translate.
    """
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )

    async for text in text_stream:
        response = translate_client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        yield {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_lang": source_lang,
            "target_lang": target_lang,
        }
