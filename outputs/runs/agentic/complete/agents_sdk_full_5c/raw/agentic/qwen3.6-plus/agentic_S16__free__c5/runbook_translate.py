"""
runbook_translate.py - Translate secret-rotation runbook notes.

Uses OpenAI's translation capabilities via the chat completions API
to translate secret rotation runbook notes and procedures between
languages for international security operations teams.

Provider: OpenAI Chat Completions API (api.openai.com)
Model: gpt-4o
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

# Provider-specific OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = "gpt-4o"


def get_openai_client() -> Optional[OpenAI]:
    """Create an OpenAI client for the chat completions API."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY environment variable not set")
        return None
    client = OpenAI(api_key=OPENAI_API_KEY)
    return client


@dataclass
class RunbookEntry:
    """A single runbook note or procedure step."""
    entry_id: str
    section: str
    original_text: str
    translated_text: str = ""
    source_language: str = "en"
    target_language: str = ""
    translation_confidence: float = 0.0
    metadata: Dict[str, str] = field(default_factory=dict)


RUNBOOK_SYSTEM_PROMPT = (
    "You are a technical translator specializing in security operations, "
    "secret management, and IT infrastructure documentation. Translate the "
    "provided runbook text accurately while preserving technical terminology, "
    "secret identifiers, and command syntax. Do not translate code blocks, "
    "ARNs, API endpoints, or secret key names. Keep the structure and "
    "formatting intact."
)


def translate_runbook_text(
    text: str,
    target_language: str,
    source_language: str = "en",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> Tuple[str, float]:
    """
    Translate a single runbook text entry using OpenAI's gpt-4o model.

    Args:
        text: The runbook text to translate.
        target_language: Target language code (e.g., 'ja', 'de', 'fr').
        source_language: Source language code (default: 'en').
        model: The OpenAI model ID for translation (default: gpt-4o).

    Returns:
        Tuple of (translated_text, confidence_score).
    """
    client = get_openai_client()
    if not client:
        return text, 0.0

    user_prompt = (
        f"Translate the following secret rotation runbook text from "
        f"{source_language} to {target_language}:\n\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": RUNBOOK_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        translated = response.choices[0].message.content.strip() if response.choices else text
        confidence = 0.9  # GPT-4o provides high-quality translations

        return translated, confidence
    except Exception as e:
        logger.error("OpenAI translation API error: %s", e)
        return text, 0.0


def translate_runbook_entries(
    entries: List[RunbookEntry],
    target_language: str,
    source_language: str = "en",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> List[RunbookEntry]:
    """
    Translate a batch of runbook entries using OpenAI's gpt-4o model.

    Processes entries sequentially to preserve context and quality.

    Args:
        entries: List of RunbookEntry objects to translate.
        target_language: Target language code.
        source_language: Source language code (default: 'en').
        model: The OpenAI model ID (default: gpt-4o).

    Returns:
        List of RunbookEntry objects with translations populated.
    """
    for entry in entries:
        entry.target_language = target_language
        entry.source_language = source_language
        translated_text, confidence = translate_runbook_text(
            entry.original_text,
            target_language,
            source_language,
            model,
        )
        entry.translated_text = translated_text
        entry.translation_confidence = confidence

    return entries


def translate_runbook_sections(
    sections: Dict[str, str],
    target_language: str,
    source_language: str = "en",
) -> Dict[str, RunbookEntry]:
    """
    Translate an entire runbook organized by sections.

    Args:
        sections: Dictionary mapping section names to their text content.
        target_language: Target language code.
        source_language: Source language code (default: 'en').

    Returns:
        Dictionary mapping section names to translated RunbookEntry objects.
    """
    entries = []
    for section_name, text in sections.items():
        entry = RunbookEntry(
            entry_id=f"section-{section_name}",
            section=section_name,
            original_text=text,
        )
        entries.append(entry)

    translated_entries = translate_runbook_entries(
        entries, target_language, source_language
    )

    return {e.section: e for e in translated_entries}


ROTATION_RUNBOOK_TEMPLATE = {
    "prerequisites": (
        "Ensure you have AWS CLI configured with appropriate IAM permissions "
        "(secretsmanager:RotateSecret). Verify the Lambda rotation function "
        "is deployed and has the correct execution role."
    ),
    "pre_rotation_checks": (
        "1. Check current secret version with describe-secret.\n"
        "2. Verify the target database or service is accessible.\n"
        "3. Confirm no active deployments depend on the current credential."
    ),
    "rotation_steps": (
        "1. Call rotate-secret API to initiate rotation.\n"
        "2. Monitor the rotation Lambda execution via CloudWatch Logs.\n"
        "3. Verify AWSPENDING stage has the new credentials.\n"
        "4. Test connectivity with the new credentials.\n"
        "5. Confirm AWSCURRENT stage transitions to the new version."
    ),
    "post_rotation_validation": (
        "1. Verify applications can authenticate with the new secret.\n"
        "2. Check CloudWatch metrics for authentication failures.\n"
        "3. Review audit logs in CloudTrail for any access anomalies.\n"
        "4. Update documentation with the rotation timestamp."
    ),
    "rollback_procedure": (
        "If rotation fails, the previous version remains accessible via "
        "the AWSPREVIOUS stage. Restore it by calling put-secret-value "
        "with the previous secret string."
    ),
}


def get_standard_runbook_translations(
    target_language: str,
) -> Dict[str, RunbookEntry]:
    """
    Get a standard secret rotation runbook translated to the target language.

    Uses the predefined ROTATION_RUNBOOK_TEMPLATE.

    Args:
        target_language: Target language code (e.g., 'ja', 'de', 'es').

    Returns:
        Dictionary of section name to translated RunbookEntry.
    """
    return translate_runbook_sections(
        ROTATION_RUNBOOK_TEMPLATE,
        target_language=target_language,
        source_language="en",
    )


def format_translated_runbook(
    translated_sections: Dict[str, RunbookEntry],
) -> str:
    """
    Format translated runbook entries into a readable document.
    """
    lines = []
    for entry in sorted(translated_sections.values(), key=lambda e: e.section):
        lines.append(f"## {entry.section}")
        lines.append(f"   [Translated to: {entry.target_language}, Confidence: {entry.translation_confidence:.2f}]")
        lines.append(f"   {entry.translated_text}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    translations = get_standard_runbook_translations("ja")
    report = format_translated_runbook(translations)
    print(report)
