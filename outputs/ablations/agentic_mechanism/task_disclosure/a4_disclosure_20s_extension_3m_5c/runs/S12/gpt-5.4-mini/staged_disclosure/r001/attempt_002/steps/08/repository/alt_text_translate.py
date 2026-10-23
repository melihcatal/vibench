import json
import os
import sys
from urllib import request, error


def translate_alt_text(text, target_language="en"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": "gpt-5.4-mini",
        "input": [
            {
                "role": "system",
                "content": "Translate image descriptions accurately and naturally. Preserve meaning, tone, and concise alt-text style.",
            },
            {
                "role": "user",
                "content": f"Translate this image description to {target_language}: {text}",
            },
        ],
    }

    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise RuntimeError(f"OpenAI API error: {exc.read().decode('utf-8', 'ignore')}") from exc

    output = data.get("output", [])
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                return content.get("text", "")

    raise RuntimeError("No translation returned by OpenAI")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: alt_text_translate.py <text> [target_language]")
    text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    print(translate_alt_text(text, target_language))


if __name__ == "__main__":
    main()
