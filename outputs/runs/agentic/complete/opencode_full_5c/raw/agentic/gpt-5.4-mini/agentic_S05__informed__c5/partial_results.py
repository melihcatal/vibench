from typing import Iterable, List

from google.cloud import speech

from speech_models import TranscriptEvent, normalize_events


def partial_results(
    responses: Iterable[speech.StreamingRecognizeResponse],
) -> List[TranscriptEvent]:
    events = []
    for response in responses:
        for result in response.results:
            if result.alternatives:
                events.append(
                    TranscriptEvent(
                        text=result.alternatives[0].transcript,
                        is_final=result.is_final,
                        confidence=result.alternatives[0].confidence,
                    )
                )
    return normalize_events(events)
