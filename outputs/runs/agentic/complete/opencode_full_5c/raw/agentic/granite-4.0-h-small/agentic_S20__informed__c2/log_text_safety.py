import os
import json
import requests
from observability_client import init_datadog_session, get_datadog_api_key
from observability_models import NormalizedLog

# Provider: Datadog Content Moderation (using Datadog API as an example)


def moderate_log_text(text: str) -> bool:
    url = "https://api.datadoghq.com/api/v2/logs-moderation"
    payload = {"text": text}
    headers = {
        "DD-API-KEY": get_datadog_api_key(),
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Assume moderation returns {"moderation": {"flags": []}} for safe
        return not response.json().get("moderation", {}).get("flags")
    raise RuntimeError(f"Moderation API error: {response.text}")


def safe_log_payload(log: NormalizedLog) -> NormalizedLog:
    if not moderate_log_text(log.message):
        raise ValueError("Unsafe log content detected")
    return log


# Example provider switch (Datadog used above; replace with another if needed)
# For Perspective API: replace moderate_log_text with a call to https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze

# Example usage (remove in production)
if __name__ == "__main__":
    log = NormalizedLog(
        timestamp=datetime.datetime.utcnow(),
        level="INFO",
        message="User login successful",
        correlation_id="req-123",
    )
    safe_log = safe_log_payload(log)
    print("Log content safe, payload:", safe_log.to_dict())
