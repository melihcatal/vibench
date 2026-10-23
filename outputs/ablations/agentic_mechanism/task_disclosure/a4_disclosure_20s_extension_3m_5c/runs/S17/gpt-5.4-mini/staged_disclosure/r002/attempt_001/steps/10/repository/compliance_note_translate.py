import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")

def translate_compliance_note(text: str, target_language: str = "en") -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    url = f"{OPENAI_API_BASE.rstrip('/')}/v1/responses"
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Translate compliance and encryption notes faithfully for reviewers. Preserve meaning, terminology, and any security-relevant details."
            },
            {
                "role": "user",
                "content": f"Translate the following note to {target_language}:\n\n{text}"
            },
        ],
    }
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                texts.append(content.get("text", ""))
    if texts:
        return "".join(texts).strip()
    return data.get("output_text", "").strip()
