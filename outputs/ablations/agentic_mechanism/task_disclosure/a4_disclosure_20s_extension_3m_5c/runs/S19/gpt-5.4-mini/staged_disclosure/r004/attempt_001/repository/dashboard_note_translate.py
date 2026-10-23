import os
import json
import urllib.request
import urllib.error


def translate_dashboard_note(note: str, target_locale: str, source_locale: str = "en") -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_API_KEY is required")

    url = "https://api-free.deepl.com/v2/translate"
    data = urllib.parse.urlencode(
        {
            "auth_key": api_key,
            "text": note,
            "target_lang": target_locale.upper(),
            "source_lang": source_locale.upper(),
        }
    ).encode("utf-8")

    request = urllib.request.Request(url, data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepL translation failed: {exc.code} {body}") from exc

    translations = payload.get("translations") or []
    if not translations:
        raise RuntimeError("DeepL translation response missing translations")
    return translations[0]["text"]


def translate_metric_note(note: str, target_locale: str, source_locale: str = "en") -> str:
    return translate_dashboard_note(note, target_locale, source_locale)
