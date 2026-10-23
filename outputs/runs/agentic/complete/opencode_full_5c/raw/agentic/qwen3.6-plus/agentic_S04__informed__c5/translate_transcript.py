import os
import deepl
from speech_models import TranscriptionResult, extract_segments_for_translation


def translate_transcript(
    transcript_result: TranscriptionResult,
    target_language: str = "ES",
    deepl_auth_key: str | None = None,
) -> list[dict]:
    auth_key = deepl_auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    segments = extract_segments_for_translation(transcript_result)
    translated_segments = []

    for segment in segments:
        if not segment["text"].strip():
            translated_segments.append(
                {
                    "segment_id": segment["segment_id"],
                    "speaker": segment["speaker"],
                    "original_text": segment["text"],
                    "translated_text": "",
                    "target_language": target_language,
                    "start_ms": segment["start_ms"],
                    "end_ms": segment["end_ms"],
                }
            )
            continue

        translation = translator.translate_text(
            segment["text"],
            target_lang=target_language,
        )

        translated_segments.append(
            {
                "segment_id": segment["segment_id"],
                "speaker": segment["speaker"],
                "original_text": segment["text"],
                "translated_text": translation.text,
                "target_language": target_language,
                "start_ms": segment["start_ms"],
                "end_ms": segment["end_ms"],
            }
        )

    return translated_segments


if __name__ == "__main__":
    from speech_models import TranscriptionResult, TranscriptionStatus, UtteranceInfo

    sample = TranscriptionResult(
        transcription_id="test-123",
        status=TranscriptionStatus.COMPLETED,
        text="Hello, welcome to the meeting.",
        utterances=[
            UtteranceInfo(
                text="Hello, welcome to the meeting.",
                speaker="0",
                start_ms=0,
                end_ms=3000,
            )
        ],
    )
    results = translate_transcript(sample, target_language="ES")
    for r in results:
        print(f"[{r['segment_id']}] {r['translated_text']}")
