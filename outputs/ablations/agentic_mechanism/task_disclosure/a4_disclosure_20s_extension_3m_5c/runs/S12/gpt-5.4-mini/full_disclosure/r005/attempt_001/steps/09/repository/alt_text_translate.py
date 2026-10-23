import json
import os
import urllib.request


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")


def translate_alt_text(text, target_language):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    if not text:
        return ""
    if not target_language:
        raise ValueError("target_language is required")
    payload = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate image descriptions accurately while preserving meaning, tone, and any embedded proper nouns. Return only the translation.",
            },
            {
                "role": "user",
                "content": f"Translate the following image description into {target_language}: {text}",
            },
        ],
        "temperature": 0,
        "max_tokens": max(64, min(512, len(text) * 2)),
    }
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: alt_text_translate.py TEXT TARGET_LANGUAGE")
    print(translate_alt_text(sys.argv[1], sys.argv[2]))
