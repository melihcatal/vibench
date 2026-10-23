from typing import Iterable, List

from speech_models import TranscriptEvent, TranscriptSegment, normalize_transcript_events


def handle_partial_and_final_events(events: Iterable[TranscriptEvent]) -> List[TranscriptSegment]:
    normalized = normalize_transcript_events(events)
    segments: List[TranscriptSegment] = []
    current_text = []
    for event in normalized:
        if event.is_partial:
            current_text = [event.text]
            segments.append(TranscriptSegment(text=event.text, is_final=False, confidence=event.confidence))
        else:
            text = event.text if event.text else " ".join(current_text)
            segments.append(TranscriptSegment(text=text, is_final=True, confidence=event.confidence))
            current_text = []
    return segments
