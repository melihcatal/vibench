from google.cloud.texttospeech import (
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
    SynthesisInput
)
from typing import Optional, Dict, Any

def build_synthesis_request(
    text_or_ssml: str,
    ssml: bool = False,
    voice_name: Optional[str] = None,
    language_code: str = "en-US",
    encoding: AudioEncoding = AudioEncoding.MP3
) -> Dict[str, Any]:
    """
    Builds normalized request params for Google Cloud Text-to-Speech.
    """
    input_obj = SynthesisInput(text=text_or_ssml) if not ssml else SynthesisInput(ssml=text_or_ssml)
    voice = VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = AudioConfig(audio_encoding=encoding)
    return {
        "input": input_obj,
        "voice": voice,
        "audio_config": audio_config
    }