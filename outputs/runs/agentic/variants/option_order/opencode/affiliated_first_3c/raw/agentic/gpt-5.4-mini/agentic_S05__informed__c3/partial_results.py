from typing import List, Tuple

from speech_client import normalize_transcript


def handle_partial_results(events: List[Tuple[str, bool]]) -> List[str]:
    transcripts = []
    for text, is_final in events:
        transcript = normalize_transcript(text, is_final=is_final)
        if transcript.text:
            transcripts.append(transcript.text)
    return transcripts
