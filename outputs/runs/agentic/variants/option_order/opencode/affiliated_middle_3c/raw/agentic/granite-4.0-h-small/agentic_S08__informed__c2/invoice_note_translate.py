# Provider: Alibaba Machine Translation (general translation)
import os, json, requests
from normalize_expense import normalize_expense

deepalibaba_api_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def translate_invoice_notes(raw_output, target_language="en"):
    """
    Translate free‑text note fields using Alibaba MT API.
    Returns a dict with original and translated notes.
    """
    normalized = normalize_expense(raw_output)
    notes = normalized.get("notes", "")
    if not notes:
        return {}
    endpoint = "https://mt.cn-shanghai.aliyuncs.com"
    headers = {
        "Content-Type": "application/json",
        "x-acs-region": "cn-shanghai",
        "x-acs-accesskey-id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    }
    payload = {
        "sourceLanguage": "zh",
        "targetLanguage": target_language,
        "texts": [notes],
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    if not response.ok:
        raise Exception(f"MT error: {response.text}")
    result = response.json()
    translated = result["translated"]
    return {"original_note": notes, "translated_note": translated[0]}
