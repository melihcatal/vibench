"""Check secret labels and notes for unsafe text using OpenAI Moderation API."""

import os
import openai
from openai import OpenAI
from security_models import SecretLabel, SecretError


# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client for the moderation API."""
    if not OPENAI_API_KEY:
        raise SecretError(
            secret_id="openai_config",
            message="OPENAI_API_KEY environment variable is not set",
            error_code="MISSING_API_KEY",
            provider="openai",
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def check_label_safety(label: SecretLabel) -> dict:
    """Check a secret label and its notes for unsafe content using OpenAI Moderation.

    Sends the label key, value, and notes to the OpenAI moderation endpoint
    (model: omni-moderation-latest) and returns the moderation result.

    Args:
        label: The SecretLabel to check.

    Returns:
        Dict with keys:
            - flagged: bool indicating if content was flagged
            - categories: dict of category flags from OpenAI moderation
            - label_key: the label key that was checked
            - label_value_masked: masked version of the label value
            - provider: "openai"
    """
    text_to_check = f"Label key: {label.key}\nLabel value: {label.value}\nNotes: {label.notes}"

    client = _get_openai_client()
    try:
        moderation_response = client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text_to_check,
        )
        result = moderation_response.results[0]
        return {
            "flagged": result.flagged,
            "categories": dict(result.categories),
            "category_scores": {
                k: float(v) for k, v in result.category_scores.items()
            },
            "label_key": label.key,
            "label_value_masked": label.value[:4] + "****" if len(label.value) > 4 else "****",
            "provider": "openai",
        }
    except openai.APIError as exc:
        raise SecretError(
            secret_id=label.secret_id,
            message=f"OpenAI moderation API error: {exc}",
            error_code="OPENAI_API_ERROR",
            provider="openai",
        )


def check_labels_safety(labels: list[SecretLabel]) -> list[dict]:
    """Check multiple secret labels for unsafe content via OpenAI Moderation API.

    Args:
        labels: List of SecretLabel objects to check.

    Returns:
        List of moderation result dicts for each label.
    """
    results = []
    for label in labels:
        result = check_label_safety(label)
        results.append(result)
    return results


def filter_unsafe_labels(labels: list[SecretLabel]) -> tuple[list[SecretLabel], list[dict]]:
    """Filter labels, returning safe labels and flagged label details.

    Uses OpenAI moderation model omni-moderation-latest to check each label.

    Returns:
        Tuple of (safe_labels, flagged_results)
    """
    safe_labels = []
    flagged_results = []
    for label in labels:
        result = check_label_safety(label)
        if result["flagged"]:
            flagged_results.append(result)
        else:
            safe_labels.append(label)
    return safe_labels, flagged_results


if __name__ == "__main__":
    test_label = SecretLabel(
        key="environment",
        value="production",
        secret_id="prod/api/key",
        notes="Main API key for prod service",
    )
    result = check_label_safety(test_label)
    print(f"Label safety check (OpenAI moderation): flagged={result['flagged']}")
