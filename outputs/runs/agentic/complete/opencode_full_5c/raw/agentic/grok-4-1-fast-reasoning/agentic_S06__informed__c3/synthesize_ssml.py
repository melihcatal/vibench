from speech_client import get_tts_client
from speech_models import build_ssml_input, build_voice, build_audio_config
from google.cloud import texttospeech


def synthesize_ssml(
    ssml: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D"
) -> bytes:
    client = get_tts_client()
    synthesis_input = build_ssml_input(ssml)
    voice = build_voice(language_code, voice_name)
    audio_config = build_audio_config()
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
