from __future__ import annotations

from typing import Iterable, Iterator, Tuple

from google.cloud import speech_v1p1beta1 as speech

from speech_models import NormalizedStreamingEvent, normalize_transcript


def handle_partial_and_final_results(responses: Iterable[speech.StreamingRecognizeResponse]) -> Iterator[Tuple[str, bool]]:
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            transcript = normalize_transcript(result.alternatives[0].transcript)
            yield transcript, bool(result.is_final)


def as_events(responses: Iterable[speech.StreamingRecognizeResponse]) -> Iterator[NormalizedStreamingEvent]:
    for transcript, is_final in handle_partial_and_final_results(responses):
        yield NormalizedStreamingEvent(transcript=transcript, final=is_final)
