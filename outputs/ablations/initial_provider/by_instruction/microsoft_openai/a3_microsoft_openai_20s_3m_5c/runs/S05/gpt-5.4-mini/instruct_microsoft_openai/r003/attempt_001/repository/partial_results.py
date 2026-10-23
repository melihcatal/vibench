from typing import Iterable, List

from speech_models import TranscriptChunk, normalize_text


def handle_partial_and_final_events(events: Iterable[TranscriptChunk]) -> List[str]:
    outputs: List[str] = []
    buffer = ""
    for event in events:
        text = normalize_text(event.text)
        if not text:
            continue
        if event.is_final:
            outputs.append(text)
            buffer = ""
        else:
            buffer = text
            outputs.append(buffer)
    return outputs
