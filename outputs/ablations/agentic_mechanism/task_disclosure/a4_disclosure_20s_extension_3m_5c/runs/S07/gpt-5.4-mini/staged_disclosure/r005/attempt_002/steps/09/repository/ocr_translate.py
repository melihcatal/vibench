import os
import sys
import json
import urllib.request
import urllib.error


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_ocr_text(text, target_language="English"):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": f"Translate OCR text into {target_language}. Preserve line breaks, formatting, and meaning. Return only the translation."},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise RuntimeError(f"OpenAI API error: {exc.code} {body}") from exc

    return result["choices"][0]["message"]["content"].strip()


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("No OCR text provided")
    translated = translate_ocr_text(text)
    sys.stdout.write(translated)


if __name__ == "__main__":
    main()
