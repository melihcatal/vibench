import os
import json
import urllib.request
import urllib.error


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_alt_text(description: str, target_language: str = "es") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Translate the following image description into "
        f"{target_language}. Preserve meaning, concise alt-text style, and do not add extra commentary.\n\n"
        f"Description: {description}"
    )

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You translate image descriptions into concise alt text."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
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

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {detail}") from exc

    return data["choices"][0]["message"]["content"].strip()
