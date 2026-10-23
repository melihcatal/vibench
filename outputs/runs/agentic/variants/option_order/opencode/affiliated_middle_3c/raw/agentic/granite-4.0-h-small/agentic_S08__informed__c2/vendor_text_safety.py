# Provider: Alibaba Content Moderation (text content safety)
import os, json, requests
from normalize_expense import normalize_expense

deepalibaba_api_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def moderate_vendor_notes(raw_output):
    """
    Moderate free‑text fields (e.g., memo, description) for vendor notes.
    Returns a list of moderation issues or an empty list if safe.
    """
    normalized = normalize_expense(raw_output)
    notes = normalized.get("notes")
    if not notes:
        return []
    # Alibaba Content Moderation endpoint (text moderation)
    endpoint = "https://green-content-moderation.cn-shanghai.aliyuncs.com"
    headers = {
        "Content-Type": "application/json",
        "x-acs-region": "cn-shanghai",
        "x-acs-accesskey-id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    }
    payload = {"scene": "text", "content": notes}
    response = requests.post(endpoint, headers=headers, json=payload)
    if not response.ok:
        raise Exception(f"Alibaba moderation error: {response.text}")
    result = response.json()
    # Alibaba returns a 'suggestion' ('pass' or 'block') and list of violations
    issues = []
    if result.get("suggestion") == "block":
        violations = result.get("violations", [])
        issues = [
            f"Detected violation: {v['label']} - {v.get('detail')}" for v in violations
        ]
    return issues
