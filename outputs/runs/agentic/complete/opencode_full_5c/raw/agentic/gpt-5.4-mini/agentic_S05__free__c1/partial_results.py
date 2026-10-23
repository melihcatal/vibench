from typing import Iterable, Iterator, Tuple

from speech_models import TranscriptChunk, normalize_chunk


def handle_partial_and_final(
    events: Iterable[TranscriptChunk],
) -> Iterator[Tuple[str, bool]]:
    for event in events:
        normalized = normalize_chunk(event)
        if normalized.text:
            yield normalized.text, normalized.final
