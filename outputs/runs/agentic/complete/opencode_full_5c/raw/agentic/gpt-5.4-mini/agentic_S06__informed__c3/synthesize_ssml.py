from speech_client import synthesize_ssml_payload


def synthesize_ssml(ssml: str, voice: str | None = None) -> bytes:
    return synthesize_ssml_payload(ssml, voice=voice)
