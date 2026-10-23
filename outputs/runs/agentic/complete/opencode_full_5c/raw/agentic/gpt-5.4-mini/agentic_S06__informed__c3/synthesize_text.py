from speech_client import synthesize_text_payload


def synthesize_text(text: str, voice: str | None = None) -> bytes:
    return synthesize_text_payload(text, voice=voice)
