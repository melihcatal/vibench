from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_text


def handle_partial_and_final(events: Iterable[dict]) -> List[TranscriptEvent]:
    output: List[TranscriptEvent] = []
    for event in events:
        text = normalize_text(event.get("text") or event.get("transcript"))
        output.append(
            TranscriptEvent(
                text=text,
                is_final=bool(event.get("is_final")),
                language=event.get("language"),
            )
        )
    return output
