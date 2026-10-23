from typing import Iterable, List

from speech_models import TranscriptSegment, normalize_transcript_text


def handle_partial_results(events: Iterable[TranscriptSegment]) -> List[str]:
    outputs = []
    for event in events:
        text = normalize_transcript_text(event.text)
        if text:
            outputs.append(text if event.is_final else f"{text}...")
    return outputs
