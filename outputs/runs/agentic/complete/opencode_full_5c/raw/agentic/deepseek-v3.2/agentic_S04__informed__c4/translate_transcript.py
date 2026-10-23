import os
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError


def translate_transcript_segments(
    segments: List[Dict[str, Any]],
    target_language_code: str = "es",
    source_language_code: str = "auto",
) -> List[Dict[str, Any]]:
    translate_client = boto3.client(
        "translate",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    translated_segments = []

    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            translated_segments.append({**segment, "translated_text": ""})
            continue

        try:
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
            )

            translated_segments.append(
                {
                    **segment,
                    "translated_text": response["TranslatedText"],
                    "source_language": response.get(
                        "SourceLanguageCode", source_language_code
                    ),
                    "target_language": target_language_code,
                }
            )

        except ClientError as e:
            print(f"Error translating segment: {e}")
            translated_segments.append(
                {**segment, "translated_text": "", "error": str(e)}
            )

    return translated_segments


def translate_transcript_text(
    text: str, target_language_code: str = "es", source_language_code: str = "auto"
) -> Dict[str, Any]:
    translate_client = boto3.client(
        "translate",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )

        return {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", source_language_code),
            "target_language": target_language_code,
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to translate text: {e}")


def batch_translate_segments(
    segments: List[Dict[str, Any]],
    target_language_code: str = "es",
    source_language_code: str = "auto",
) -> List[Dict[str, Any]]:
    translate_client = boto3.client(
        "translate",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    translated_segments = []

    for i in range(0, len(segments), 10):
        batch = segments[i : i + 10]

        for segment in batch:
            text = segment.get("text", "")
            if not text.strip():
                translated_segments.append({**segment, "translated_text": ""})
                continue

            try:
                response = translate_client.translate_text(
                    Text=text,
                    SourceLanguageCode=source_language_code,
                    TargetLanguageCode=target_language_code,
                )

                translated_segments.append(
                    {
                        **segment,
                        "translated_text": response["TranslatedText"],
                        "source_language": response.get(
                            "SourceLanguageCode", source_language_code
                        ),
                        "target_language": target_language_code,
                    }
                )

            except ClientError as e:
                print(f"Error translating batch segment: {e}")
                translated_segments.append(
                    {**segment, "translated_text": "", "error": str(e)}
                )

    return translated_segments
