# key_usage_summary.py
# Summarize crypto key usage and events using the Watsonx guardrails / HAP detection service

import os
import requests
from datetime import datetime

# Provider: watsonx guardrails / HAP detection (watsonx.ai)
# Expected env vars: WATSONX_API_KEY, WATSONX_PROJECT_ID

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError(
        "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
    )

guardrails_url = "https://api.watsonx.ibm.com/guardrails/v1/detect"


def summarize_key_usage(events: list[dict]) -> dict:
    """Accept a list of event dictionaries with fields:\n    - key_name (str)\n    - operation (str, e.g., ENC, DEC, SIGN, VERIFY)\n    - timestamp (ISO 8601 string)\n    Returns a condensed summary JSON with counts per operation and any guardrails alerts."""
    payload = {
        "project_id": WATSONX_PROJECT_ID,
        "content": [asdict(ev) for ev in events],  # convert to plain dicts for JSON
    }
    headers = {
        "Authorization": f"Bearer {WATSONX_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(guardrails_url, json=payload, headers=headers)
    resp.raise_for_status()
    guardrails_resp = resp.json()
    # Guardrails may add fields like \"issues\" or \"summary\"
    usage_summary = {
        "total_events": len(events),
        "counts": {
            ev["operation"]: sum(1 for e in events if e["operation"] == ev["operation"])
            for ev in events
        },
        "alerts": guardrails_resp.get("issues", []),
    }
    return usage_summary


if __name__ == "__main__":
    # Simple demo usage
    sample_events = [
        {
            "key_name": "my-data-encrypt-key",
            "operation": "ENC",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        {
            "key_name": "my-data-encrypt-key",
            "operation": "DEC",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        {
            "key_name": "signature-key",
            "operation": "SIGN",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    ]
    print(summarize_key_usage(sample_events))
