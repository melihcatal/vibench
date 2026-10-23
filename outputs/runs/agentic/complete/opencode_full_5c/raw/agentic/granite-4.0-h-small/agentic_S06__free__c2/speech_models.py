from typing import TypedDict


class SynthesizeRequest(TypedDict):
    """Normalized request payload for Text-to-Speech."""

    input: dict  # either {'text': str} or {'ssml': str}
    voice: dict  # {'languageCode': str, 'name': str}
    audioConfig: dict  # {'audioEncoding': str}


class SynthesizeResponse(TypedDict):
    """Normalized response from provider."""

    audio_content: bytes


# Simple normalization helper


def normalize_request(request_type: str, **kwargs) -> SynthesizeRequest:
    """
    Build a standardized request dict understood by our provider wrappers.
    Possible kwargs:
        - text: plain text
        - ssml: SSML markup
        - voice_language_code / voice_name
        - audio_encoding
    """
    input_payload = {}
    if "text" in kwargs:
        input_payload["text"] = kwargs["text"]
    elif "ssml" in kwargs:
        input_payload["ssml"] = kwargs["ssml"]
    else:
        raise ValueError("Either 'text' or 'ssml' must be provided")

    voice_payload = {
        "languageCode": kwargs.get("voice_language_code", "en-US"),
        "name": kwargs.get("voice_name", "en-US-Wavenet-D"),
    }

    audio_config = {"audioEncoding": kwargs.get("audio_encoding", "MP3")}

    return {"input": input_payload, "voice": voice_payload, "audioConfig": audio_config}
