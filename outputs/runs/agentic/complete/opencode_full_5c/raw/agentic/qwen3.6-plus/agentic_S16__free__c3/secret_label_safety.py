from typing import Optional
import os
import requests

from security_models import SafetyCheckResult
from security_client import get_vault_client


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL_ID = "omni-moderation-latest"


def check_label_safety(
    secret_path: str, label_name: str, mount_point: Optional[str] = None
) -> SafetyCheckResult:
    client = get_vault_client()
    try:
        response = client.read_secret(
            client._build_secret_url(secret_path, mount_point).split("/data/")[-1]
        )
        labels = response.labels
    finally:
        client.close()

    label_value = labels.get(label_name, "")
    return _moderate_label(secret_path, label_name, label_value)


def _moderate_label(
    secret_path: str, label_name: str, label_value: str
) -> SafetyCheckResult:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return SafetyCheckResult(
            secret_path=secret_path,
            label_name=label_name,
            label_value=label_value,
            is_safe=True,
            explanation="OpenAI API key not configured, skipping moderation",
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL_ID,
        "input": label_value,
    }

    resp = requests.post(
        OPENAI_MODERATION_URL, json=payload, headers=headers, timeout=30
    )
    resp.raise_for_status()
    result = resp.json()

    results = result.get("results", [])
    if not results:
        return SafetyCheckResult(
            secret_path=secret_path,
            label_name=label_name,
            label_value=label_value,
            is_safe=True,
        )

    moderation = results[0]
    flagged = moderation.get("flagged", False)
    categories = moderation.get("categories", {})
    flagged_categories = [k for k, v in categories.items() if v]

    return SafetyCheckResult(
        secret_path=secret_path,
        label_name=label_name,
        label_value=label_value,
        is_safe=not flagged,
        categories=categories,
        flagged_categories=flagged_categories,
        explanation=f"Label {'flagged' if flagged else 'passed'} moderation check",
    )


def check_all_labels_safety(
    secret_path: str, mount_point: Optional[str] = None
) -> list[SafetyCheckResult]:
    client = get_vault_client()
    try:
        response = client.read_secret(
            client._build_secret_url(secret_path, mount_point).split("/data/")[-1]
        )
        labels = response.labels
    finally:
        client.close()

    results = []
    for label_name, label_value in labels.items():
        result = _moderate_label(secret_path, label_name, str(label_value))
        results.append(result)
    return results


if __name__ == "__main__":
    import os

    secret_path = os.environ.get(
        "LABEL_CHECK_SECRET_PATH", "prod/services/auth-service"
    )
    label_name = os.environ.get("LABEL_NAME", "description")
    result = check_label_safety(secret_path, label_name)
    print(result.to_dict())
