import os
import requests
from observability_client import get_config

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def metric_annotation_safety(text):
    if not OPENAI_API_KEY:
        return {"safe": False, "reason": "missing OPENAI_API_KEY", "model": OPENAI_MODEL}
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODEL, "messages": [{"role": "system", "content": "Classify whether the input is safe, non-malicious dashboard or metric annotation text."}, {"role": "user", "content": text}], "temperature": 0}
    r = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
