import google.cloud.texttospeech_v1.types as tts_types
from google.cloud.texttospeech_v1.types import AudioEncoding, SsmlVoiceGender
from typing import Optional

def create_synthesis_input(text: Optional[str] = None, ssml: Optional[str] = None) -> tts_types.SynthesisInput:
    if text is not None and ssml is not None:
        raise ValueError("Specify either text or ssml, not both.")
    if text is not None:
        return tts_types.SynthesisInput(text=text)
    if ssml is not None:
        return tts_types.SynthesisInput(ssml=ssml)
    raise ValueError("Must specify text or ssml.")

def create_voice_selection_params(
    language_code: str,
    name: Optional[str] = None,
    ssml_gender_str: Optional[str] = None
) -> tts_types.VoiceSelectionParams:
    params = tts_types.VoiceSelectionParams(language_code=language_code)
    if name:
        params.name = name
    if ssml_gender_str:
        try:
            gender = SsmlVoiceGender[ssml_gender_str.upper()]
            params.ssml_gender = gender
        except KeyError:
            raise ValueError(f"Invalid ssml_gender: {ssml_gender_str}. Must be one of {list(SsmlVoiceGender.__members__.keys())}")
    return params

def create_audio_config(
    audio_encoding: str = "MP3",
    speaking_rate: Optional[float] = None,
    pitch: Optional[float] = None,
    volume_gain_db: Optional[float] = None,
    sample_rate_hertz: Optional[int] = None,
    bitrate_bps: Optional[int] = None
) -> tts_types.AudioConfig:
    encoding_map = {
        "MP3": AudioEncoding.MP3,
        "OGG_OPUS": AudioEncoding.OGG_OPUS,
        "LINEAR16": AudioEncoding.LINEAR16,
    }
    config = tts_types.AudioConfig(audio_encoding=encoding_map[audio_encoding.upper()])
    if speaking_rate is not None:
        config.speaking_rate = speaking_rate
    if pitch is not None:
        config.pitch = pitch
    if volume_gain_db is not None:
        config.volume_gain_db = volume_gain_db
    if sample_rate_hertz is not None:
        config.sample_rate_hertz = sample_rate_hertz
    if bitrate_bps is not None:
        config.bitrate_bps = bitrate_bps
    return config
