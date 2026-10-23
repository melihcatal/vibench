from speech_models import TranscriptEvent


def handle_partial_and_final(event):
    transcript_event = TranscriptEvent.from_payload(event)
    if transcript_event.is_final:
        return {"final": transcript_event.text, "partial": None}
    return {"final": None, "partial": transcript_event.text}
