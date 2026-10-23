import os
import deepl
from speech_models import TranscriptionResult


def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return deepl.Translator(auth_key)


def translate_transcript_segments(
    segments: list[dict],
    target_language: str = "ES",
    source_language: str | None = None,
) -> list[dict]:
    translator = get_deepl_client()

    translated_segments = []
    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            translated_segments.append(segment)
            continue

        result = translator.translate_text(
            text,
            target_lang=target_language,
            source_lang=source_language,
        )

        translated_segment = dict(segment)
        translated_segment["translated_text"] = result.text
        translated_segment["target_language"] = target_language
        translated_segments.append(translated_segment)

    return translated_segments


def translate_full_transcript(
    transcript_result: TranscriptionResult,
    target_language: str = "ES",
) -> TranscriptionResult:
    translated_result = TranscriptionResult(
        transcript_id=transcript_result.transcript_id,
        status=transcript_result.status,
        text="",
        words=transcript_result.words,
        utterances=transcript_result.utterances,
        confidence=transcript_result.confidence,
        audio_duration=transcript_result.audio_duration,
        language_code=target_language.lower(),
    )

    if transcript_result.utterances:
        segments = [
            {"text": u.text, "speaker": u.speaker} for u in transcript_result.utterances
        ]
        translated = translate_transcript_segments(segments, target_language)
        translated_result.text = " ".join(t["translated_text"] for t in translated)
    elif transcript_result.text:
        translator = get_deepl_client()
        result = translator.translate_text(
            transcript_result.text,
            target_lang=target_language,
        )
        translated_result.text = result.text

    return translated_result


if __name__ == "__main__":
    segments = [
        {"text": "Hello, welcome to the meeting.", "speaker": "Speaker A"},
        {"text": "Thank you for joining us today.", "speaker": "Speaker B"},
    ]
    translated = translate_transcript_segments(segments, target_language="ES")
    for seg in translated:
        print(f"[{seg.get('speaker', 'N/A')}] {seg['translated_text']}")
