from speech_client import get_tts_client
from speech_models import make_voice_params, make_audio_config
from google.cloud.texttospeech_v1 import SynthesisInput, AudioEncoding


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str = None,
    encoding: AudioEncoding = AudioEncoding.MP3,
) -> bytes:
    client = get_tts_client()
    synthesis_input = SynthesisInput(text=text)
    voice_params = make_voice_params(language_code=language_code, name=voice_name)
    audio_config = make_audio_config(encoding=encoding)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content
