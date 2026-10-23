from __future__ import annotations

import os

import requests

from security_models import SafetyFinding

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"


def check_secret_label_safety(label: str, notes: str) -> SafetyFinding:
    endpoint = os.getenv(AZURE_CONTENT_SAFETY_ENDPOINT_ENV, "")
    key = os.getenv(AZURE_CONTENT_SAFETY_KEY_ENV, "")
    url = endpoint.rstrip("/") + "/contentsafety/text:analyze?api-version=2023-10-01"
    payload = {"text": f"label: {label}\nnotes: {notes}"}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    unsafe = bool(data.get("blocklistsMatch") or data.get("hate", {}).get("severity", 0) >= 2)
    reason = "Azure AI Content Safety flagged the text" if unsafe else "No unsafe content detected by Azure AI Content Safety"
    return SafetyFinding(label=label, unsafe=unsafe, reason=reason)
