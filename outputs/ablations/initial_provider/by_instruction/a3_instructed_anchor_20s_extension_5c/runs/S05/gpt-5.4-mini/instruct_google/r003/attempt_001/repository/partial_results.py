from typing import Iterable, List, Tuple

from speech_models import TranscriptChunk, normalize_text


def handle_partial_and_final(results: Iterable[TranscriptChunk]) -> Tuple[List[str], str]:
    partials: List[str] = []
    finals: List[str] = []
    for result in results:
        text = normalize_text(result.text)
        if not text:
            continue
        if result.is_final:
            finals.append(text)
        else:
            partials.append(text)
    return partials, " ".join(finals)
