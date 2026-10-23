from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_events


def handle_partial_results(events: Iterable[TranscriptEvent]) -> List[str]:
    normalized = normalize_events(events)
    rendered = []
    for event in normalized:
        prefix = "FINAL" if event.is_final else "PARTIAL"
        rendered.append(f"{prefix}: {event.text}")
    return rendered
