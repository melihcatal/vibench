from text_to_speech_client import text_to_speech


def reviewer_brief_audio(text):
    audio = text_to_speech.synthesize_speech(text)
    return audio
