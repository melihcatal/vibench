import os
from dataclasses import dataclass, field
from typing import List, Optional
import deepl

from speech_models import TranscriptSegment, TranscriptSegments


@dataclass
class TranslatedSegment:
    index: int
    speaker: str
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class TranslatedSegments:
    segments: List[TranslatedSegment]
    target_language: str
    total_segments: int


def translate_transcript(
    segments: TranscriptSegments,
    target_language: str = "es",
    auth_key: str = None,
) -> TranslatedSegments:
    if auth_key is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY", "")

    translator = deepl.Translator(auth_key)

    translated = []
    for seg in segments.segments:
        if seg.text.strip():
            result = translator.translate_text(
                seg.text,
                target_lang=target_language.upper(),
            )
            translated.append(
                TranslatedSegment(
                    index=seg.index,
                    speaker=seg.speaker,
                    original_text=seg.text,
                    translated_text=result.text,
                    target_language=target_language,
                )
            )
        else:
            translated.append(
                TranslatedSegment(
                    index=seg.index,
                    speaker=seg.speaker,
                    original_text="",
                    translated_text="",
                    target_language=target_language,
                )
            )

    return TranslatedSegments(
        segments=translated,
        target_language=target_language,
        total_segments=len(translated),
    )


if __name__ == "__main__":
    from speech_models import TranscriptSegment, TranscriptSegments

    sample = TranscriptSegments(
        segments=[
            TranscriptSegment(
                index=0,
                speaker="Speaker A",
                text="Welcome to the meeting.",
                start_ms=0,
                end_ms=3000,
            ),
            TranscriptSegment(
                index=1,
                speaker="Speaker B",
                text="Thank you for having me.",
                start_ms=3500,
                end_ms=6000,
            ),
        ],
        total_segments=2,
    )
    translated = translate_transcript(sample, target_language="es")
    for seg in translated.segments:
        print(f"[{seg.speaker}] {seg.translated_text}")
