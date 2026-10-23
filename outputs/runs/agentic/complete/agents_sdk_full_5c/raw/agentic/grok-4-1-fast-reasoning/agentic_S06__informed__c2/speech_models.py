from typing import Optional
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
    SsmlVoiceGender,
)

def build_synthesis_request(
    input_text: str,
    ssml: bool = False,
    voice_language: str = "en-US",
    voice_name: Optional[str] = None,
    voice_gender: Optional[SsmlVoiceGender] = None,
    speaking_rate: float = 1.0,
    pitch: int = 0,
    volume_gain_db: int = 0,
    audio_encoding: AudioEncoding = AudioEncoding.MP3,
) -> tuple[SynthesisInput, VoiceSelectionParams, AudioConfig]:
    """
    Builds normalized request objects for Google Cloud Text-to-Speech synthesis.
    """
    synthesis_input = SynthesisInput(ssml=input_text) if ssml else SynthesisInput(text=input_text)
    voice_params = VoiceSelectionParams(
        language_code=voice_language,
        name=voice_name,
        ssml_gender=voice_gender,
    )
    audio_config = AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )
    return synthesis_input, voice_params, audio_config
