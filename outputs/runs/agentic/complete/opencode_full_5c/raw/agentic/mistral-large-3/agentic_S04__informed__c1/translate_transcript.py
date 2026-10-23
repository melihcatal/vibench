import os
from typing import List, Dict
import boto3
from botocore.exceptions import ClientError


def translate_transcript(
    transcript_segments: List[Dict[str, str]], target_language: str
) -> List[Dict[str, str]]:
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    translated_segments = []
    for segment in transcript_segments:
        try:
            response = translate_client.translate_text(
                Text=segment["text"],
                SourceLanguageCode="auto",
                TargetLanguageCode=target_language,
            )
            translated_segments.append(
                {
                    "text": response["TranslatedText"],
                    "start": segment["start"],
                    "end": segment["end"],
                }
            )
        except ClientError as e:
            raise Exception(f"Failed to translate segment: {e}")
    return translated_segments
