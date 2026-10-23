from speech_client import get_tts_client
from speech_models import make_voice_params, make_audio_config
from google.cloud.texttospeech_v1 import SynthesisInput, AudioEncoding


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str = None,
    encoding: AudioEncoding = AudioEncoding.MP3,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> bytes:
    client = get_tts_client()
    synthesis_input = SynthesisInput(ssml=ssml)
    voice_params = make_voice_params(language_code=language_code, name=voice_name)
    audio_config = make_audio_config(
        encoding=encoding, speaking_rate=speaking_rate, pitch=pitch
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content
