from typing import Dict, List

from speech_models import SpeechTranscript, transcript_from_event


def handle_partial_and_final_events(events: List[Dict]) -> Dict[str, List[str]]:
    partials: List[str] = []
    finals: List[str] = []
    for event in events:
        transcript = transcript_from_event(event)
        if transcript.is_final:
            finals.append(transcript.text)
        else:
            partials.append(transcript.text)
    return {"partials": partials, "finals": finals}
