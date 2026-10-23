from safety_client import synthesize_audio as google_synthesize_audio


def reviewer_brief_audio(text):
    return google_synthesize_audio(text)
