from typing import Iterable, Iterator

from speech_models import TranscriptEvent, normalize_transcript


def handle_partial_and_final(events: Iterable[TranscriptEvent]) -> Iterator[str]:
    partial = []
    for event in events:
        text = normalize_transcript(event.text)
        if not text:
            continue
        if event.is_final:
            if partial:
                partial.clear()
            yield text
        else:
            partial.append(text)
            yield text
