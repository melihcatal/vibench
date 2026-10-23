"""
Translate secret-rotation runbook notes using Amazon Translate.

Translates operational runbook documentation for secret rotation procedures
between languages to support international security operations teams.

Provider: Amazon Translate
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
from typing import Optional, Dict, Any, List

import boto3
from botocore.exceptions import ClientError

# Amazon Translate provider configuration
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"


def _get_translate_client(region: Optional[str] = None) -> boto3.client:
    """Create an Amazon Translate boto3 client."""
    region_name = region or os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION)

    access_key = os.environ.get(AWS_ACCESS_KEY_ID_ENV)
    secret_key = os.environ.get(AWS_SECRET_ACCESS_KEY_ENV)

    if not access_key or not secret_key:
        raise ValueError(
            f"AWS credentials not found. Set {AWS_ACCESS_KEY_ID_ENV} and "
            f"{AWS_SECRET_ACCESS_KEY_ENV} environment variables."
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name,
    )

    return session.client("translate")


def translate_runbook_note(
    text: str,
    source_language: str = "en",
    target_language: str = "ja",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a single runbook note using Amazon Translate.

    Args:
        text: The runbook note text to translate.
        source_language: Source language code (BCP-47 or ISO 639).
        target_language: Target language code.
        region: Optional AWS region override.

    Returns:
        Dictionary with the translated text and metadata.
    """
    try:
        client = _get_translate_client(region=region)

        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        result = {
            "success": True,
            "translated_text": response.get("TranslatedText", ""),
            "source_language": response.get("SourceLanguageCode", source_language),
            "target_language": response.get("TargetLanguageCode", target_language),
            "provider": "amazon_translate",
            "original_length": len(text),
            "translated_length": len(response.get("TranslatedText", "")),
        }
        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return {
            "success": False,
            "error_code": error_code,
            "error_message": error_message,
            "provider": "amazon_translate",
            "source_language": source_language,
            "target_language": target_language,
        }
    except Exception as e:
        return {
            "success": False,
            "error_code": "TRANSLATE_CLIENT_ERROR",
            "error_message": str(e),
            "provider": "amazon_translate",
            "source_language": source_language,
            "target_language": target_language,
        }


def translate_runbook_notes_batch(
    notes: List[Dict[str, Any]],
    target_language: str = "ja",
    source_language: str = "en",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a batch of runbook notes using Amazon Translate.

    Each note dict should have 'note_id' and 'text' keys. Amazon Translate
    is called sequentially for each note (batch translate jobs are for S3 files).

    Args:
        notes: List of dicts with 'note_id' and 'text' keys.
        target_language: Target language code for all translations.
        source_language: Source language code for all translations.
        region: Optional AWS region override.

    Returns:
        Dictionary with batch translation results.
    """
    translations = []
    errors = []

    for note in notes:
        note_id = note.get("note_id", "unknown")
        text = note.get("text", "")

        if not text.strip():
            translations.append({
                "note_id": note_id,
                "original_text": "",
                "translated_text": "",
                "skipped": True,
            })
            continue

        result = translate_runbook_note(
            text=text,
            source_language=source_language,
            target_language=target_language,
            region=region,
        )

        if result.get("success"):
            translations.append({
                "note_id": note_id,
                "original_text": text,
                "translated_text": result["translated_text"],
                "source_language": result["source_language"],
                "target_language": result["target_language"],
            })
        else:
            errors.append({
                "note_id": note_id,
                "error_code": result.get("error_code", ""),
                "error_message": result.get("error_message", ""),
            })

    return {
        "success": len(errors) == 0,
        "total_notes": len(notes),
        "successfully_translated": len(translations),
        "failed": len(errors),
        "translations": translations,
        "errors": errors,
        "provider": "amazon_translate",
        "target_language": target_language,
        "source_language": source_language,
    }


def translate_runbook_section(
    section_title: str,
    section_steps: List[str],
    target_language: str = "es",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a complete runbook section (title + steps) using Amazon Translate.

    Args:
        section_title: The section heading to translate.
        section_steps: List of step descriptions to translate.
        target_language: Target language code.
        region: Optional AWS region override.

    Returns:
        Dictionary with the translated section.
    """
    title_result = translate_runbook_note(
        text=section_title,
        target_language=target_language,
        region=region,
    )

    step_results = []
    for idx, step in enumerate(section_steps, 1):
        step_result = translate_runbook_note(
            text=step,
            target_language=target_language,
            region=region,
        )
        step_results.append({
            "step_number": idx,
            "original": step,
            "translated": step_result.get("translated_text", step),
            "success": step_result.get("success", False),
        })

    return {
        "success": title_result.get("success", False) and all(s["success"] for s in step_results),
        "section_title": {
            "original": section_title,
            "translated": title_result.get("translated_text", section_title),
        },
        "steps": step_results,
        "target_language": target_language,
        "provider": "amazon_translate",
    }
