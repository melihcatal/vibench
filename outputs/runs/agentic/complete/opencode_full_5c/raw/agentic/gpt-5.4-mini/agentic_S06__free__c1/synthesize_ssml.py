from speech_client import synthesize_ssml as _synthesize_ssml


def synthesize_ssml(ssml: str, voice: str | None = None) -> bytes:
    return _synthesize_ssml(ssml, voice=voice).audio
