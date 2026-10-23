from typing import Any, Dict, Iterable, List

from speech_models import StreamingTranscriptEvent, event_from_deepgram, normalize_text


def handle_partial_and_final_events(
    events: Iterable[Dict[str, Any]],
) -> List[StreamingTranscriptEvent]:
    output: List[StreamingTranscriptEvent] = []
    for payload in events:
        event = event_from_deepgram(payload)
        if event.text:
            event.text = normalize_text(event.text)
            output.append(event)
    return output
