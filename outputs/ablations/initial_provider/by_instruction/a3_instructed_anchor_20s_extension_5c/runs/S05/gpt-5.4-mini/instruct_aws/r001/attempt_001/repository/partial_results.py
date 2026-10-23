from typing import Iterable, Iterator

from speech_models import TranscriptResult, normalize_result_payload


def handle_partial_and_final_results(events: Iterable[dict]) -> Iterator[TranscriptResult]:
    for event in events:
        for result in event.get("Transcript", {}).get("Results", []):
            yield normalize_result_payload(result)
