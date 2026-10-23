from speech_client import get_tts_client
from speech_models import create_ssml_input, create_voice_params, create_audio_config


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str = None,
    ssml_gender: str = None,
    encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> bytes:
    client = get_tts_client()
    input_ = create_ssml_input(ssml)
    voice = create_voice_params(language_code, voice_name, ssml_gender)
    audio_config = create_audio_config(
        encoding=encoding, speaking_rate=speaking_rate, pitch=pitch
    )
    response = client.synthesize_speech(
        input=input_, voice=voice, audio_config=audio_config
    )
    return response.audio_content
