import os
import json
from typing import Dict, Any, Optional, List
import boto3
from botocore.exceptions import ClientError


def translate_text(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    if not text:
        return text

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        translate_args = {
            "Text": text,
            "SourceLanguageCode": source_language if source_language else "auto",
            "TargetLanguageCode": target_language,
        }

        response = translate_client.translate_text(**translate_args)

        return response["TranslatedText"]

    except ClientError as e:
        raise Exception(f"Failed to translate text with Amazon Translate: {e}")


def translate_message_payload(
    payload: Dict[str, Any],
    target_language: str = "es",
    fields_to_translate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    translated_payload = payload.copy()

    if fields_to_translate is None:
        fields_to_translate = [
            "text",
            "content",
            "message",
            "description",
            "comment",
            "feedback",
        ]

    if "data" in translated_payload and isinstance(translated_payload["data"], dict):
        for field in fields_to_translate:
            if field in translated_payload["data"] and isinstance(
                translated_payload["data"][field], str
            ):
                try:
                    translated_text = translate_text(
                        translated_payload["data"][field], target_language
                    )
                    translated_payload["data"][field] = translated_text
                    translated_payload["data"][f"{field}_original"] = payload["data"][
                        field
                    ]
                    translated_payload["data"][f"{field}_translated"] = True
                    translated_payload["data"][f"{field}_target_language"] = (
                        target_language
                    )
                except Exception as e:
                    print(f"Failed to translate field '{field}': {e}")
                    translated_payload["data"][f"{field}_translation_error"] = str(e)

    elif isinstance(translated_payload.get("text"), str):
        try:
            translated_text = translate_text(
                translated_payload["text"], target_language
            )
            translated_payload["text_translated"] = translated_text
            translated_payload["text_original"] = payload["text"]
            translated_payload["text_target_language"] = target_language
        except Exception as e:
            print(f"Failed to translate text field: {e}")
            translated_payload["text_translation_error"] = str(e)

    translated_payload["translation_metadata"] = {
        "target_language": target_language,
        "translation_timestamp": "2024-01-15T10:30:00Z",
        "translation_service": "Amazon Translate",
    }

    return translated_payload


def batch_translate_messages(
    messages: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    translated_messages = []

    for i, message in enumerate(messages):
        try:
            translated_msg = translate_message_payload(message, target_language)
            translated_messages.append(translated_msg)
        except Exception as e:
            print(f"Failed to translate message {i}: {e}")
            message["translation_error"] = str(e)
            translated_messages.append(message)

    return translated_messages


def detect_language(text: str) -> str:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        response = comprehend_client.detect_dominant_language(Text=text)

        if response["Languages"]:
            top_language = response["Languages"][0]
            return top_language["LanguageCode"]
        else:
            return "unknown"

    except ClientError as e:
        raise Exception(f"Failed to detect language with Amazon Comprehend: {e}")


def translate_with_language_detection(
    payload: Dict[str, Any], target_language: str = "es"
) -> Dict[str, Any]:
    text_to_analyze = ""

    if "data" in payload and isinstance(payload["data"], dict):
        for field in ["text", "content", "message"]:
            if field in payload["data"] and isinstance(payload["data"][field], str):
                text_to_analyze = payload["data"][field]
                break

    if not text_to_analyze and isinstance(payload.get("text"), str):
        text_to_analyze = payload["text"]

    source_language = None
    if text_to_analyze:
        try:
            source_language = detect_language(text_to_analyze)
        except Exception as e:
            print(f"Language detection failed: {e}")

    if source_language and source_language != target_language:
        return translate_message_payload(payload, target_language)
    else:
        payload["translation_metadata"] = {
            "source_language": source_language or "unknown",
            "target_language": target_language,
            "translation_required": source_language != target_language
            if source_language
            else False,
            "translation_service": "Amazon Translate",
        }
        return payload


if __name__ == "__main__":
    sample_messages = [
        {
            "id": "msg_001",
            "data": {
                "user_feedback": "The product quality is excellent and delivery was fast.",
                "rating": 5,
                "category": "positive_feedback",
            },
        },
        {
            "id": "msg_002",
            "data": {
                "complaint": "The item arrived damaged and customer service was unhelpful.",
                "urgency": "high",
                "category": "complaint",
            },
        },
    ]

    try:
        print("Translating messages to Spanish:")

        for i, msg in enumerate(sample_messages):
            print(f"\nOriginal message {msg['id']}:")
            print(json.dumps(msg["data"], indent=2))

            translated = translate_message_payload(msg, "es")
            print(f"\nTranslated message {msg['id']}:")
            print(json.dumps(translated["data"], indent=2))

        print("\n\nBatch translation:")
        batch_translated = batch_translate_messages(sample_messages, "fr")
        for msg in batch_translated:
            print(f"\nMessage {msg.get('id')}:")
            if "translation_metadata" in msg:
                print(f"  Translation metadata: {msg['translation_metadata']}")

    except Exception as e:
        print(f"Error: {e}")
