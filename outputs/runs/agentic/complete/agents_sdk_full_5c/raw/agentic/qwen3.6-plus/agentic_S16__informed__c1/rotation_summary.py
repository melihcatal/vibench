"""
Summarize secret rotation status using Mistral Chat API.

Generates a human-readable summary of AWS Secrets Manager rotation metadata
including rotation schedule, pending versions, and rotation history.

Provider: Mistral Chat API
SDK: mistralai
Auth: MISTRAL_API_KEY
Model: mistral-large-latest
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from mistralai import Mistral


MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_API_KEY_ENV = "MISTRAL_API_KEY"


def _build_rotation_summary_prompt(rotation_data: List[Dict[str, Any]]) -> str:
    """Build a prompt for the Mistral model to summarize rotation data."""
    entries = []
    for idx, data in enumerate(rotation_data, 1):
        entry_lines = [f"Secret #{idx}: {data.get('secret_id', 'unknown')}"]
        if data.get("rotation_enabled"):
            entry_lines.append(f"  - Rotation: ENABLED")
            if data.get("rotation_rules"):
                rules = data["rotation_rules"]
                interval = rules.get("automatically_after_days", "N/A")
                entry_lines.append(f"  - Rotation interval: Every {interval} days")
            if data.get("last_rotated_date"):
                entry_lines.append(f"  - Last rotated: {data['last_rotated_date']}")
            if data.get("next_rotation"):
                entry_lines.append(f"  - Next rotation: {data['next_rotation']}")
            if data.get("rotation_lambda_arn"):
                entry_lines.append(f"  - Rotation Lambda: {data['rotation_lambda_arn']}")
        else:
            entry_lines.append("  - Rotation: DISABLED")

        if data.get("version_stages"):
            stages = data["version_stages"]
            entry_lines.append(f"  - Version stages: {json.dumps(stages)}")
            if "AWSPENDING" in str(stages):
                entry_lines.append("  - WARNING: Pending version exists (rotation may be in progress)")

        entries.append("\n".join(entry_lines))

    prompt = (
        "You are a security operations assistant. Summarize the following secret rotation "
        "status data from AWS Secrets Manager.\n\n"
        "Provide:\n"
        "1. A brief overview of the rotation posture across all secrets.\n"
        "2. Any secrets that have rotation disabled and should be reviewed.\n"
        "3. Any secrets with pending versions indicating in-progress rotations.\n"
        "4. Recommendations for improving the rotation posture.\n\n"
        "Rotation data:\n\n"
    )
    prompt += "\n\n".join(entries)
    return prompt


def summarize_rotation_status(
    rotation_data: List[Dict[str, Any]],
    model: str = MISTRAL_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Generate a summary of secret rotation status using Mistral Chat API.

    Args:
        rotation_data: List of secret rotation metadata dictionaries from
            AWS Secrets Manager describe_secret or list operations.
        model: Mistral model identifier (default: mistral-large-latest).
        max_tokens: Maximum tokens for the response.
        temperature: Sampling temperature for generation.

    Returns:
        Dictionary with the generated summary and metadata.
    """
    api_key = os.environ.get(MISTRAL_API_KEY_ENV)
    if not api_key:
        return {
            "success": False,
            "error_code": "MISSING_API_KEY",
            "error_message": f"Set the {MISTRAL_API_KEY_ENV} environment variable.",
        }

    client = Mistral(api_key=api_key)

    prompt = _build_rotation_summary_prompt(rotation_data)

    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a security operations analyst specializing in "
                        "AWS Secrets Manager rotation best practices."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        summary_text = ""
        if chat_response and chat_response.choices:
            summary_text = chat_response.choices[0].message.content or ""

        result = {
            "success": True,
            "summary": summary_text,
            "model_used": model,
            "provider": "mistralai",
            "secrets_analyzed": len(rotation_data),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return result

    except Exception as e:
        return {
            "success": False,
            "error_code": "MISTRAL_API_ERROR",
            "error_message": str(e),
            "provider": "mistralai",
            "model_used": model,
        }


def summarize_single_secret_rotation(
    secret_metadata: Dict[str, Any],
    model: str = MISTRAL_MODEL,
) -> Dict[str, Any]:
    """
    Generate a rotation summary for a single secret using Mistral.

    Args:
        secret_metadata: Single secret rotation metadata dict.
        model: Mistral model identifier.

    Returns:
        Dictionary with the generated summary.
    """
    return summarize_rotation_status(
        rotation_data=[secret_metadata],
        model=model,
    )
