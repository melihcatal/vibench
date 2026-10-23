from typing import Optional, Union
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
)


def build_synthesis_request(
    text_or_ssml: Union[str, None] = None,
    ssml: Optional[str] = None,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    encoding: AudioEncoding = AudioEncoding.MP3,
) -> tuple[SynthesisInput, VoiceSelectionParams, AudioConfig]:
    if ssml:
        synthesis_input = SynthesisInput(ssml=ssml)
    elif text_or_ssml:
        synthesis_input = SynthesisInput(text=text_or_ssml)
    else:
        raise ValueError("Must provide text or ssml")

    voice = VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = AudioConfig(audio_encoding=encoding)

    return synthesis_input, voice, audio_config
