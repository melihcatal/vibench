from typing import List

from speech_models import TranscriptEvent, normalize_text


def handle_partial_results(events: List[dict]) -> List[TranscriptEvent]:
    results: List[TranscriptEvent] = []
    for event in events:
        results.append(
            TranscriptEvent(
                text=normalize_text(event.get("text", "")),
                is_final=bool(event.get("final", False)),
                language=event.get("language"),
                confidence=event.get("confidence"),
            )
        )
    return results
