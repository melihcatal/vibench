from typing import Iterable, List

from speech_models import RecognitionEvent, normalize_transcript


def handle_partial_results(events: Iterable[RecognitionEvent]) -> List[str]:
    partials: List[str] = []
    final_text = []
    for event in events:
        text = normalize_transcript(event.text)
        if not text:
            continue
        if event.is_final:
            final_text.append(text)
        else:
            partials.append(text)
    return partials + final_text
