from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    CHAT_ENDPOINT,
    get_headers,
    validate_api_key,
)
from speech_models import (
    TranslatedSegment,
    TranscriptionResult,
)


def translate_segments(
    segments: list,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    translated = []
    for i, seg in enumerate(segments):
        text = seg.text if hasattr(seg, "text") else seg.get("text", "")
        if not text.strip():
            continue

        src_lang = source_language or "auto-detect"

        system_prompt = (
            f"You are a professional translator. Translate the following text to {target_language}. "
            f"Preserve the original meaning, tone, and formatting. "
            f"Return only the translated text."
        )

        response = httpx.post(
            CHAT_ENDPOINT,
            headers=get_headers(),
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                "temperature": 0.3,
                "max_tokens": 1000,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()

        translated_text = data["choices"][0]["message"]["content"].strip()

        translated.append(
            TranslatedSegment(
                original_text=text,
                translated_text=translated_text,
                source_language=src_lang,
                target_language=target_language,
                segment_id=seg.id if hasattr(seg, "id") else i,
            )
        )

    return translated


def translate_transcript(
    transcript: TranscriptionResult,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    segments = transcript.segments if transcript.segments else []
    if not segments:
        segments = [{"text": transcript.text, "id": 0}]

    return translate_segments(
        segments=segments,
        target_language=target_language,
        source_language=source_language or transcript.language,
        model=model,
    )


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 2:
        transcript_file = sys.argv[1]
        target_lang = sys.argv[2]

        with open(transcript_file, "r") as f:
            data = json.load(f)

        transcript = TranscriptionResult(
            text=data.get("text", ""),
            language=data.get("language", ""),
            duration=data.get("duration", 0.0),
            segments=data.get("segments", []),
        )

        results = translate_transcript(transcript, target_language=target_lang)
        for seg in results:
            print(f"[{seg.segment_id}] {seg.original_text}")
            print(f"  -> {seg.translated_text}")
    else:
        print(
            "Usage: python translate_transcript.py <transcript.json> <target_language>"
        )
