import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError
from security_models import CryptoAuditNote


def translate_compliance_notes(
    notes: List[CryptoAuditNote], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """
    Translate encryption or compliance notes for reviewers using Amazon Translate.
    """
    # AWS credentials are read from environment variables:
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

    # Validate AWS credentials
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    if not notes:
        return []

    # Initialize AWS Translate client
    try:
        translate_client = boto3.client(
            "translate", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
    except Exception as e:
        raise ValueError(f"Failed to initialize AWS Translate client: {str(e)}")

    results = []

    for note in notes:
        try:
            # Prepare text for translation
            # Include metadata in the translation for context
            text_to_translate = f"""
            Audit Note ID: {note.note_id}
            Operation: {note.operation}
            Key Identifier: {note.key_id}
            Severity Level: {note.severity}
            Associated Tags: {", ".join(note.tags) if note.tags else "none"}
            
            Note Content:
            {note.note_text}
            
            Timestamp: {note.timestamp.isoformat()}
            """

            # Call Amazon Translate
            response = translate_client.translate_text(
                Text=text_to_translate.strip(),
                SourceLanguageCode="auto",  # Auto-detect source language
                TargetLanguageCode=target_language,
            )

            translated_text = response["TranslatedText"]
            source_language = response["SourceLanguageCode"]

            results.append(
                {
                    "note_id": note.note_id,
                    "original_text": note.note_text,
                    "translated_text": translated_text,
                    "source_language": source_language,
                    "target_language": target_language,
                    "operation": note.operation,
                    "key_id": note.key_id,
                    "severity": note.severity,
                    "tags": note.tags,
                    "timestamp": note.timestamp.isoformat(),
                    "provider": "amazon-translate",
                    "service": "aws",
                    "success": True,
                }
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]

            results.append(
                {
                    "note_id": note.note_id,
                    "original_text": note.note_text,
                    "translated_text": None,
                    "operation": note.operation,
                    "key_id": note.key_id,
                    "severity": note.severity,
                    "tags": note.tags,
                    "timestamp": note.timestamp.isoformat(),
                    "provider": "amazon-translate",
                    "service": "aws",
                    "success": False,
                    "error": f"AWS Translate error ({error_code}): {error_message}",
                }
            )

        except Exception as e:
            results.append(
                {
                    "note_id": note.note_id,
                    "original_text": note.note_text,
                    "translated_text": None,
                    "operation": note.operation,
                    "key_id": note.key_id,
                    "severity": note.severity,
                    "tags": note.tags,
                    "timestamp": note.timestamp.isoformat(),
                    "provider": "amazon-translate",
                    "service": "aws",
                    "success": False,
                    "error": str(e),
                }
            )

    return results


def translate_single_note(
    note_text: str, target_language: str = "es", context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Translate a single compliance note with optional context.
    """
    # AWS credentials are read from environment variables
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    try:
        translate_client = boto3.client(
            "translate", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )

        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            full_text = f"Context:\n{context_str}\n\nNote:\n{note_text}"
        else:
            full_text = note_text

        response = translate_client.translate_text(
            Text=full_text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )

        return {
            "original_text": note_text,
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": target_language,
            "provider": "amazon-translate",
            "service": "aws",
            "success": True,
            "applied_context": context is not None,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        return {
            "original_text": note_text,
            "translated_text": None,
            "target_language": target_language,
            "provider": "amazon-translate",
            "service": "aws",
            "success": False,
            "error": f"AWS Translate error ({error_code}): {error_message}",
            "applied_context": context is not None,
        }
    except Exception as e:
        return {
            "original_text": note_text,
            "translated_text": None,
            "target_language": target_language,
            "provider": "amazon-translate",
            "service": "aws",
            "success": False,
            "error": str(e),
            "applied_context": context is not None,
        }
