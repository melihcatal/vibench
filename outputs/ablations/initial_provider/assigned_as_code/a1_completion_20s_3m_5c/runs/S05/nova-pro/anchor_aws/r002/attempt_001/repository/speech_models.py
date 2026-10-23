def normalize_transcript(transcript):
    return transcript.get("text", "").strip()

def is_final(transcript):
    return transcript.get("is_final", False)

def normalize_event(event):
    return event