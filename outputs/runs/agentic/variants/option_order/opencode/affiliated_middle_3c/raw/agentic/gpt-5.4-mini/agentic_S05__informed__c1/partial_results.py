from typing import Iterable, List

from speech_models import TranscriptEvent, event_from_result


def handle_partial_and_final(results: Iterable[object]) -> List[TranscriptEvent]:
    events: List[TranscriptEvent] = []
    for result in results:
        event = event_from_result(result)
        if event.text:
            events.append(event)
    return events
