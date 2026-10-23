from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud.speech_v1.types import StreamingRecognizeResponse

from speech_models import TranscriptAlternative, TranscriptEvent, normalize_transcript_text


def iter_transcript_events(
    responses: Iterable[StreamingRecognizeResponse],
) -> Iterator[TranscriptEvent]:
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            primary = result.alternatives[0]
            text = normalize_transcript_text(primary.transcript)
            if not text:
                continue
            alternatives = [
                TranscriptAlternative(
                    transcript=normalize_transcript_text(alt.transcript),
                    confidence=getattr(alt, "confidence", None),
                )
                for alt in result.alternatives
            ]
            yield TranscriptEvent(
                text=text,
                is_final=bool(result.is_final),
                confidence=getattr(primary, "confidence", None),
                raw=result,
                alternatives=alternatives,
            )


def latest_interim_text(responses: Iterable[StreamingRecognizeResponse]) -> str:
    text = ""
    for event in iter_transcript_events(responses):
        if not event.is_final:
            text = event.text
    return text


def collect_final_transcript(responses: Iterable[StreamingRecognizeResponse]) -> str:
    return " ".join(event.text for event in iter_transcript_events(responses) if event.is_final)
