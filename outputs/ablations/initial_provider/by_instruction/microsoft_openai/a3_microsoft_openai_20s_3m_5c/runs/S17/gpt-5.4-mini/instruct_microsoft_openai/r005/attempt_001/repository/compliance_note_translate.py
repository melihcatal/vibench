import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def compliance_note_translate(note: str, target_language: str = "en") -> dict:
    config = load_security_config()
    response = requests.post(OPENAI_RESPONSES_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": config["openai_model"], "input": f"Translate this encryption or compliance note to {target_language} for reviewers: {normalize_text(note)}"}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "language": target_language, "translation": normalize_text(data.get("output_text") or note)}


if __name__ == "__main__":
    print(json.dumps(compliance_note_translate(normalize_text(os.getenv("NOTE", "")), normalize_text(os.getenv("TARGET_LANGUAGE", "en")))))
