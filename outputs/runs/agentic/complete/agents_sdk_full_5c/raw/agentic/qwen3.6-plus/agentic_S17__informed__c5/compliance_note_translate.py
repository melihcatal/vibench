"""
[LATER-STEP] compliance_note_translate.py

Translates encryption or compliance notes for reviewers using Amazon Translate.
Provider: Amazon Translate | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses the TranslateText API to translate compliance documentation and
encryption-related notes between language pairs.
"""

import os
import sys
import logging
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def _build_translate_client() -> boto3.client:
    """Build an Amazon Translate client using environment credentials."""
    return boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def translate_text(
    text: str,
    source_language_code: str,
    target_language_code: str,
) -> str:
    """
    Translate a text string using Amazon Translate.

    Args:
        text: Source text to translate.
        source_language_code: ISO 639-1 code for source language (e.g., 'en').
        target_language_code: ISO 639-1 code for target language (e.g., 'es').

    Returns:
        Translated text string.

    Raises:
        RuntimeError: If the translate call fails.
    """
    client = _build_translate_client()

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
    except ClientError as exc:
        logger.error("Amazon Translate failed: %s", exc)
        raise RuntimeError(f"Translation failed: {exc}") from exc

    return response.get("TranslatedText", "")


def translate_compliance_notes(
    notes: List[str],
    source_language: str = "en",
    target_language: str = "es",
) -> List[Dict]:
    """
    Translate a list of compliance notes.

    Args:
        notes: List of compliance/encryption note strings.
        source_language: Source language code.
        target_language: Target language code.

    Returns:
        List of dicts with 'original', 'translated', 'source_language',
        'target_language', and optional 'error' fields.
    """
    results = []
    for note in notes:
        if not note or not note.strip():
            continue
        try:
            translated = translate_text(
                text=note.strip(),
                source_language_code=source_language,
                target_language_code=target_language,
            )
            results.append({
                "original": note,
                "translated": translated,
                "source_language": source_language,
                "target_language": target_language,
                "service": "Amazon Translate",
                "model": "amazon-translate-general",
            })
        except RuntimeError as exc:
            logger.warning("Translation failed for note: %s", exc)
            results.append({
                "original": note,
                "translated": None,
                "source_language": source_language,
                "target_language": target_language,
                "error": str(exc),
                "service": "Amazon Translate",
            })
    return results


def translate_encryption_compliance_note(
    note: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> Dict:
    """
    Translate a single encryption or compliance note for reviewers.

    Auto-detects source language if not provided by using 'auto' with
    Amazon Translate.

    Args:
        note: The compliance or encryption note text.
        target_language: Target language code.
        source_language: Optional source language code; auto-detected if omitted.

    Returns:
        Dict with translation result.
    """
    src = source_language or "auto"

    try:
        translated = translate_text(
            text=note.strip(),
            source_language_code=src,
            target_language_code=target_language,
        )
        return {
            "original": note,
            "translated": translated,
            "source_language": src,
            "target_language": target_language,
            "service": "Amazon Translate",
        }
    except RuntimeError as exc:
        return {
            "original": note,
            "translated": None,
            "source_language": src,
            "target_language": target_language,
            "error": str(exc),
            "service": "Amazon Translate",
        }


def main() -> None:
    """CLI entry point for translating compliance notes."""
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        note = sys.argv[1]
    else:
        note = sys.stdin.read().strip()

    if not note:
        print("Error: No note provided.", file=sys.stderr)
        sys.exit(1)

    target_lang = os.getenv("TRANSLATE_TARGET_LANGUAGE", "es")

    result = translate_encryption_compliance_note(note, target_language=target_lang)
    if result.get("translated"):
        print(f"Translated ({result['source_language']} -> {result['target_language']}):")
        print(result["translated"])
    else:
        print(f"Translation error: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
