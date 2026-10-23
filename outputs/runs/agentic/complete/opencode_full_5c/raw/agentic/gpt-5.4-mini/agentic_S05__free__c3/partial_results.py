import json
from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_transcript


def handle_stream_events(messages: Iterable[str]) -> List[TranscriptEvent]:
    output: List[TranscriptEvent] = []
    for message in messages:
        payload = json.loads(message)
        event = normalize_transcript(payload)
        if event.text:
            output.append(event)
    return output


def latest_partial(events: Iterable[TranscriptEvent]) -> str:
    text = ""
    for event in events:
        if not event.is_final and event.text:
            text = event.text
    return text
