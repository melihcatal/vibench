# compliance_note_translate.py
import os
from typing import Dict, Any

from security_client import SecurityClient
from security_models import SecurityModels

# AWS Translate (later-step) - translate compliance or encryption notes for reviewers


def translate_note(note: str, target_language: str = "es") -> str:
    """Translate a compliance or encryption note to the target language using AWS Translate."""
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=note, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]


def translate_audit_key(key_id: str, target_language: str = "es") -> str:
    """Translate the audit summary for a specific KMS key."""
    client = SecurityClient()
    usage = get_key_usage(key_id)  # reuse helper from key_usage_summary.py
    note = (
        f"Key ID: {key_id}, Service: AWS KMS, Usage: {usage['value']} total API calls."
    )
    return translate_note(note, target_language)


def translate_all_keys(
    key_ids: List[str], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Translate audit notes for a list of keys."""
    translated = []
    for k in key_ids:
        translated.append(
            {"key_id": k, "translated_note": translate_audit_key(k, target_language)}
        )
    return translated
