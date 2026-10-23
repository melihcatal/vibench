import os
import json
import logging
from typing import Optional

import openai
from openai import OpenAI

from security_models import SafetyCheckResult, AuditNote

logger = logging.getLogger(__name__)

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_ENDPOINT = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return OpenAI(
        api_key=api_key,
        base_url=OPENAI_API_ENDPOINT,
    )


def check_secret_label_safety(
    secret_id: str,
    label_text: str,
    model: str = OPENAI_MODEL,
) -> SafetyCheckResult:
    client = get_openai_client()

    system_prompt = (
        "You are a security analyzer for secret management systems. "
        "Analyze the provided secret label or note text and determine if it contains "
        "unsafe content such as: actual secret values, passwords, tokens, API keys, "
        "PII (personal identifiable information), or other sensitive data that should "
        "not appear in labels or notes. "
        "Respond with a JSON object containing: is_safe (boolean), flagged_items (list of strings), "
        "confidence (float 0-1), and details (string explanation)."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Analyze this secret label/note for unsafe content:\n\n{label_text}",
                },
            ],
            temperature=0.1,
            max_tokens=300,
            response_format={"type": "json_object"},
        )

        result_text = response.choices[0].message.content
        result_data = json.loads(result_text)

        safety_result = SafetyCheckResult(
            secret_id=secret_id,
            is_safe=result_data.get("is_safe", True),
            flagged_items=result_data.get("flagged_items", []),
            confidence=result_data.get("confidence", 0.0),
            details=result_data.get("details", ""),
        )

        logger.info(
            "Checked label safety via OpenAI %s: secret_id=%s, is_safe=%s, provider=openai, endpoint=%s",
            model,
            secret_id,
            safety_result.is_safe,
            OPENAI_API_ENDPOINT,
        )

        return safety_result

    except Exception as e:
        logger.error(
            "Failed to check label safety via OpenAI %s: secret_id=%s, error=%s, endpoint=%s",
            model,
            secret_id,
            str(e),
            OPENAI_API_ENDPOINT,
        )
        return SafetyCheckResult(
            secret_id=secret_id,
            is_safe=False,
            flagged_items=["analysis_failed"],
            confidence=0.0,
            details=f"Safety check failed: {str(e)}",
        )


def check_secret_labels_batch(
    audit_notes: list[AuditNote],
    model: str = OPENAI_MODEL,
) -> list[SafetyCheckResult]:
    results = []

    for note in audit_notes:
        label_text = f"Labels: {', '.join(note.labels)}\nNote: {note.note_text}"
        result = check_secret_label_safety(note.secret_id, label_text, model)
        results.append(result)

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_note = AuditNote(
        secret_id="test/api-key",
        note_text="Updated API key for production service",
        labels=["production", "api-key", "rotated-2024"],
    )
    result = check_secret_label_safety(test_note.secret_id, test_note.note_text)
    print(json.dumps(result.to_dict(), indent=2))
