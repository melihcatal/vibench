import os
import sys
import urllib.request
import urllib.error
import json


API_HOST = "https://translation.googleapis.com"


def translate_text(text: str, target_language: str, source_language: str | None = None) -> str:
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY or GOOGLE_API_KEY is required")

    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    if source_language:
        payload["source"] = source_language

    url = f"{API_HOST}/language/translate/v2?key={api_key}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Cloud Translation API error: {exc.code} {body}") from exc

    translations = result.get("data", {}).get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned from Google Cloud Translation API")
    return translations[0].get("translatedText", "")


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: alt_text_translate.py TARGET_LANGUAGE TEXT [SOURCE_LANGUAGE]")

    target_language = sys.argv[1]
    text = sys.argv[2]
    source_language = sys.argv[3] if len(sys.argv) > 3 else None
    translated = translate_text(text, target_language, source_language)
    sys.stdout.write(translated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
