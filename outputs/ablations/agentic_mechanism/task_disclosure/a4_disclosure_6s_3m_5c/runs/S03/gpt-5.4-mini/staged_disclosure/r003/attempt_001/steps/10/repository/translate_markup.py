import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _escape_text(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _split_markup(text):
    parts = []
    buf = []
    in_tag = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "<":
            if buf:
                parts.append((False, "".join(buf)))
                buf = []
            in_tag = True
            buf.append(ch)
        elif ch == ">" and in_tag:
            buf.append(ch)
            parts.append((True, "".join(buf)))
            buf = []
            in_tag = False
        else:
            buf.append(ch)
        i += 1
    if buf:
        parts.append((in_tag, "".join(buf)))
    return parts


def _translate_text_deepl(text, target_lang, source_lang=None):
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY or DEEPL_API_KEY is required")
    data = {"text": text, "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        DEEPL_API_URL,
        data=body,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}", "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", "replace")) from exc
    return payload["translations"][0]["text"]


def translate_markup(text, target_lang, source_lang=None):
    parts = _split_markup(text)
    out = []
    for is_tag, part in parts:
        if is_tag:
            out.append(part)
        elif part:
            translated = _translate_text_deepl(part, target_lang, source_lang)
            out.append(_escape_text(translated))
    return "".join(out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2:
        raise SystemExit("usage: translate_markup.py TARGET_LANG TEXT [SOURCE_LANG]")
    target_lang = argv[0]
    text = argv[1]
    source_lang = argv[2] if len(argv) > 2 else None
    sys.stdout.write(translate_markup(text, target_lang, source_lang))


if __name__ == "__main__":
    main()
