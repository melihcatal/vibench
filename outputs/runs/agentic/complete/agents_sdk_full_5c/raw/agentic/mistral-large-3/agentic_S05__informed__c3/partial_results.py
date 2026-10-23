import json
from speech_models import TranscriptEvent

def handle_partial_result(message):
    data = json.loads(message)
    if "channel" in data:
        transcript = data["channel"]["alternatives"][0]["transcript"]
        is_final = data.get("is_final", False)
        event = TranscriptEvent(transcript, is_final)
        print(f"Deepgram {'(Final)' if is_final else '(Partial)'}: {transcript}")
        return event