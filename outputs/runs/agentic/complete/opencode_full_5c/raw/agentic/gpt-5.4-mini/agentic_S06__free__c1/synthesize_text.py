from speech_client import synthesize_text as _synthesize_text


def synthesize_text(text: str, voice: str = "en-US-JennyNeural") -> bytes:
    return _synthesize_text(text, voice=voice).audio
