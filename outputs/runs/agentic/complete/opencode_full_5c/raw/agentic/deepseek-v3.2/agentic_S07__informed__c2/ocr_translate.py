import os
from typing import List, Dict, Any
import boto3
from botocore.config import Config


def translate_ocr_text(text: str, target_language: str = "en") -> str:
    """
    Translate extracted OCR text using Amazon Translate.

    Args:
        text: Text to translate
        target_language: Target language code (default: 'en' for English)

    Returns:
        Translated text
    """
    # Initialize Amazon Translate client
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(retries={"max_attempts": 3}),
    )

    # Detect source language automatically
    try:
        # First detect the language
        detect_response = translate_client.detect_text(
            Text=text[:100]  # Use first 100 chars for detection
        )
        source_language = detect_response["LanguageCode"]
    except:
        # Default to auto-detection
        source_language = "auto"

    # Translate the text
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return response["TranslatedText"]


def translate_document_sections(
    sections: List[Dict[str, Any]], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Translate multiple document sections using Amazon Translate.

    Args:
        sections: List of document sections with text
        target_language: Target language code

    Returns:
        List of translated sections
    """
    # Initialize Amazon Translate client
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    translated_sections = []

    for section in sections:
        text = section.get("text", "")
        if text:
            try:
                response = translate_client.translate_text(
                    Text=text,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=target_language,
                )

                translated_section = section.copy()
                translated_section["text"] = response["TranslatedText"]
                translated_section["original_text"] = text
                translated_section["source_language"] = response.get(
                    "SourceLanguageCode", "auto"
                )
                translated_section["target_language"] = target_language
                translated_section["provider"] = "Amazon Translate"

                translated_sections.append(translated_section)
            except Exception as e:
                # Keep original text if translation fails
                translated_section = section.copy()
                translated_section["translation_error"] = str(e)
                translated_section["provider"] = "Amazon Translate"
                translated_sections.append(translated_section)

    return translated_sections
