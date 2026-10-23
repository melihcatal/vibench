import os
from typing import Dict, List, Any, Optional
from document_models import ExpenseRecord


def translate_invoice_notes(
    notes_text: str, target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using AWS Translate.
    """
    import boto3
    from botocore.exceptions import ClientError

    # Initialize AWS Translate client
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials must be configured")

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    translation_results = {
        "original_text": notes_text,
        "translated_text": notes_text,  # Default to original
        "target_language": target_language,
        "source_language": "auto",
        "translation_provider": "aws_translate",
        "confidence": 1.0,
        "translation_timestamp": os.getenv("TRANSLATION_TIMESTAMP", ""),
    }

    try:
        # Detect source language first
        detect_response = translate_client.detect_dominant_language(Text=notes_text)

        detected_languages = detect_response["Languages"]
        if detected_languages:
            primary_language = detected_languages[0]
            source_language = primary_language["LanguageCode"]
            source_confidence = primary_language["Score"]

            translation_results["source_language"] = source_language
            translation_results["detection_confidence"] = source_confidence

            # Only translate if source language is different from target
            if source_language != target_language:
                translate_response = translate_client.translate_text(
                    Text=notes_text,
                    SourceLanguageCode=source_language,
                    TargetLanguageCode=target_language,
                )

                translation_results["translated_text"] = translate_response[
                    "TranslatedText"
                ]
                translation_results["confidence"] = translate_response.get(
                    "AppliedSettings", {}
                ).get("ConfidenceThreshold", 0.95)

                # Get additional translation metadata
                translation_results["applied_terminology_names"] = (
                    translate_response.get("AppliedTerminologies", [])
                )
                translation_results["settings"] = translate_response.get(
                    "AppliedSettings", {}
                )

        # Get supported languages for context
        list_languages_response = translate_client.list_languages()
        translation_results["supported_languages"] = [
            lang["LanguageCode"] for lang in list_languages_response["Languages"]
        ]

        # Analyze text complexity
        text_length = len(notes_text)
        word_count = len(notes_text.split())

        translation_results["text_analysis"] = {
            "character_count": text_length,
            "word_count": word_count,
            "average_word_length": text_length / word_count if word_count > 0 else 0,
            "language_complexity": "simple"
            if word_count < 50
            else "moderate"
            if word_count < 200
            else "complex",
        }

        # Check for potential translation issues
        if (
            translation_results["source_language"] == "auto"
            and translation_results["detection_confidence"] < 0.5
        ):
            translation_results["translation_warnings"] = [
                "Low confidence in language detection"
            ]

        if len(notes_text) > 5000:
            translation_results["translation_warnings"] = translation_results.get(
                "translation_warnings", []
            )
            translation_results["translation_warnings"].append(
                "Text exceeds recommended length for optimal translation"
            )

        # Add terminology information
        try:
            list_terminologies_response = translate_client.list_terminologies()
            translation_results["available_terminologies"] = [
                term["Name"]
                for term in list_terminologies_response["TerminologyPropertiesList"]
            ]
        except ClientError:
            translation_results["available_terminologies"] = []

        # Calculate translation quality metrics
        if translation_results["translated_text"] != notes_text:
            # Simple quality heuristic based on length preservation
            original_len = len(notes_text)
            translated_len = len(translation_results["translated_text"])
            length_ratio = translated_len / original_len if original_len > 0 else 1.0

            translation_results["quality_metrics"] = {
                "length_preservation_ratio": length_ratio,
                "length_preservation_status": "good"
                if 0.7 <= length_ratio <= 1.3
                else "moderate"
                if 0.5 <= length_ratio <= 1.5
                else "poor",
            }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        translation_results["error"] = (
            f"AWS Translate error: {error_code} - {error_message}"
        )
        translation_results["confidence"] = 0.0

        # Fallback: keep original text
        translation_results["translated_text"] = notes_text

    except Exception as e:
        translation_results["error"] = str(e)
        translation_results["confidence"] = 0.0
        translation_results["translated_text"] = notes_text

    return translation_results
