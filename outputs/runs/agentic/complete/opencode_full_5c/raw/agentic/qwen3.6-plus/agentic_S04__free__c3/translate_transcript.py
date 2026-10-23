import os
import requests
from typing import List, Dict, Any, Optional

from speech_models import SegmentTranslation, TranscriptionResult

DEEPL_API_BASE = "https://api-free.deepl.com/v2"
DEEPL_MODEL = "deepl-free"


def get_deepl_api_key() -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is not set")
    return api_key


def translate_segments(
    segments: List[Dict[str, Any]],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[SegmentTranslation]:
    api_key = get_deepl_api_key()

    texts = [seg.get("text", "") for seg in segments]
    if not texts:
        return []

    payload = {
        "text": texts,
        "target_lang": target_language.upper(),
    }
    if source_language:
        payload["source_lang"] = source_language.upper()

    response = requests.post(
        f"{DEEPL_API_BASE}/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data=payload,
    )
    response.raise_for_status()
    translations = response.json()["translations"]

    results = []
    for i, seg in enumerate(segments):
        translated = translations[i]["text"] if i < len(translations) else ""
        results.append(
            SegmentTranslation(
                original_text=seg.get("text", ""),
                translated_text=translated,
                source_language=source_language or "AUTO",
                target_language=target_language,
                start=seg.get("start", 0),
                end=seg.get("end", 0),
            )
        )

    return results


def translate_transcript(
    transcript_data: Dict[str, Any],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    segments = transcript_data.get("segments", [])
    if not segments:
        full_text = transcript_data.get("text", "")
        if full_text:
            segments = [{"text": full_text, "start": 0, "end": 0}]

    translated = translate_segments(segments, target_language, source_language)

    translated_text = " ".join(t.translated_text for t in translated)

    return {
        "provider": "DeepL",
        "model": DEEPL_MODEL,
        "source_language": translated[0].source_language if translated else "AUTO",
        "target_language": target_language,
        "translated_text": translated_text,
        "segment_translations": [
            {
                "original": t.original_text,
                "translated": t.translated_text,
                "start": t.start,
                "end": t.end,
            }
            for t in translated
        ],
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python translate_transcript.py <target_lang> <text>")
        sys.exit(1)

    target_lang = sys.argv[1]
    text = sys.argv[2]
    result = translate_transcript({"text": text}, target_lang)
    print(result)
