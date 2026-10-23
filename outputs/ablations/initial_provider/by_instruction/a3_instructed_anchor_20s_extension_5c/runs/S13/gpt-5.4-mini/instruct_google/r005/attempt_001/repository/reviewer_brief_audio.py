from safety_client import speech


def reviewer_brief_audio(text: str, voice: str = "alloy"):
    return speech(text, voice=voice)
