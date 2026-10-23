import json
import os
import urllib.error
import urllib.parse
import urllib.request


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_consent_copy(text: str, target_language: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Translate identity-provider consent copy faithfully and clearly."},
            {"role": "user", "content": f"Translate the following consent copy into {target_language}:\n\n{text}"},
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
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {body}") from exc

    return data["choices"][0]["message"]["content"].strip()
