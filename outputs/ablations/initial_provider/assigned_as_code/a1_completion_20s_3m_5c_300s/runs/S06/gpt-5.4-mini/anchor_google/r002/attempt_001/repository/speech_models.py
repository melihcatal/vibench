from google.cloud import texttospeech


def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    return payload or {}


def normalize_ssml_payload(payload):
    if isinstance(payload, str):
        return {"ssml": payload}
    return payload or {}


def normalize_locale(locale):
    return locale or "en-US"


def voice_to_dict(voice):
    return {
        "name": getattr(voice, "name", None),
        "language_codes": list(getattr(voice, "language_codes", [])),
        "ssml_gender": getattr(voice, "ssml_gender", None),
    }


def response_to_dict(response):
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}


def make_synthesis_input(payload):
    if "ssml" in payload:
        return texttospeech.SynthesisInput(ssml=payload["ssml"])
    return texttospeech.SynthesisInput(text=payload["text"])
