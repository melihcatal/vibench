from typing import Any
import boto3


def vendor_text_safety(text: str) -> dict:
    client = boto3.client('comprehend')
    result = client.detect_toxic_content(TextSegments=[{'Text': text}], LanguageCode='en')
    return result
