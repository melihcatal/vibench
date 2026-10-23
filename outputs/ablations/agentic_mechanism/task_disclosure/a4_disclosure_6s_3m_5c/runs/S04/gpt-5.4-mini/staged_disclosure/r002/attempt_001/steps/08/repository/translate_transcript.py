import json
import os
import sys
import urllib.error
import urllib.request


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _translate_segment(text, source_language, target_language, api_key):
    prompt = (
        f"Translate the following completed transcript segment from {source_language} to {target_language}. "
        "Preserve meaning, punctuation, names, and line breaks. Return only the translation.\n\n"
        f"{text}"
    )
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise translation engine."},
            {"role": "user", "content": prompt},
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
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"].strip()


def translate_transcript(segments, source_language="auto", target_language="English"):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    translated = []
    for segment in segments:
        if segment.get("status") != "completed":
            translated.append(segment)
            continue
        content = segment.get("text", "")
        translated_text = _translate_segment(content, source_language, target_language, api_key)
        updated = dict(segment)
        updated["translated_text"] = translated_text
        updated["translated_language"] = target_language
        translated.append(updated)
    return translated


def main():
    payload = json.load(sys.stdin)
    segments = payload if isinstance(payload, list) else payload.get("segments", [])
    source_language = payload.get("source_language", "auto") if isinstance(payload, dict) else "auto"
    target_language = payload.get("target_language", "English") if isinstance(payload, dict) else "English"
    result = translate_transcript(segments, source_language, target_language)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
