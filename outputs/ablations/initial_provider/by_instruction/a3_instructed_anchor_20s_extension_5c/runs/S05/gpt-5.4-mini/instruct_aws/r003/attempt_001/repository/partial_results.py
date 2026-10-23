from typing import Iterable, Iterator

from speech_models import TranscriptChunk, normalize_transcript_text


def handle_partial_results(events: Iterable[dict]) -> Iterator[TranscriptChunk]:
    for event in events:
        results = event.get("TranscriptEvent", {}).get("Transcript", {}).get("Results", [])
        for result in results:
            alternatives = result.get("Alternatives", [])
            if not alternatives:
                continue
            yield TranscriptChunk(
                text=normalize_transcript_text(alternatives[0].get("Transcript", "")),
                is_partial=result.get("IsPartial", False),
                language_code=event.get("language_code"),
            )
