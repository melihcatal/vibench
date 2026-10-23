from speech_client import get_tts_client
from speech_models import create_text_input, create_voice, create_audio_config
from google.cloud.texttospeech_v1 import SsmlVoiceGender
from typing import Optional


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    ssml_gender: Optional[SsmlVoiceGender] = None,
    speaking_rate: float = 1.0,
) -> bytes:
    client = get_tts_client()
    synthesis_input = create_text_input(text)
    voice = create_voice(voice_name, language_code, ssml_gender)
    audio_config = create_audio_config(speaking_rate)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
