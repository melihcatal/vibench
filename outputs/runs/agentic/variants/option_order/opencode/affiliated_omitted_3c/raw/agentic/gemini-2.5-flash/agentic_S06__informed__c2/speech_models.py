import dataclasses


@dataclasses.dataclass
class SynthesisRequest:
    text: str | None = None
    ssml: str | None = None
    voice_name: str = "en-US-JennyNeural"
    output_format: str = "audio-16khz-128kbitrate-mono-mp3"
    locale: str = "en-US"

    def __post_init__(self):
        if not self.text and not self.ssml:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if self.text and self.ssml:
            raise ValueError("Cannot provide both 'text' and 'ssml'.")


@dataclasses.dataclass
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"


@dataclasses.dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: str
    description: str | None = None


def normalize_synthesis_request(
    text: str | None = None, ssml: str | None = None, voice_name: str | None = None
) -> SynthesisRequest:
    # Example normalization logic
    if text:
        return SynthesisRequest(text=text, voice_name=voice_name or "en-US-JennyNeural")
    elif ssml:
        return SynthesisRequest(ssml=ssml, voice_name=voice_name or "en-US-JennyNeural")
    else:
        raise ValueError("Must provide either text or ssml.")


if __name__ == "__main__":
    # Example usage
    # try:
    #     request_text = normalize_synthesis_request(text="Hello world.")
    #     print(request_text)
    #     request_ssml = normalize_synthesis_request(ssml="<speak>Hello world.</speak>")
    #     print(request_ssml)
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
