from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_text


def handle_partial_and_final_events(events: Iterable[dict]) -> List[TranscriptEvent]:
    out: List[TranscriptEvent] = []
    for event in events:
        text = normalize_text(event.get("transcript") or event.get("text") or "")
        out.append(
            TranscriptEvent(
                text=text,
                is_final=bool(event.get("is_final") or event.get("final")),
                language=event.get("language"),
                confidence=event.get("confidence"),
            )
        )
    return out
