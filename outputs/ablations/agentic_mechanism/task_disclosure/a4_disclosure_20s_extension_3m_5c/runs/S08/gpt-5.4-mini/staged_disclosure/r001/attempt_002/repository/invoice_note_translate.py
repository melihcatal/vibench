import os
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_invoice_note(text: str, target_lang: str = "EN") -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing DeepL API key")
    if not text:
        return ""
    response = requests.post(
        DEEPL_API_URL,
        data={
            "auth_key": api_key,
            "text": text,
            "target_lang": target_lang,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    if not translations:
        raise RuntimeError("DeepL returned no translations")
    return translations[0]["text"]


def main() -> None:
    import sys
    source = sys.stdin.read()
    result = translate_invoice_note(source.strip())
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
