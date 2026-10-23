from google.cloud import texttospeech
from speech_models import create_text_input, create_voice, create_audio_config


def synthesize_text(
    text: str, language_code: str = "en-US", voice_name: str = None
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = create_text_input(text)
    voice = create_voice(language_code, voice_name)
    audio_config = create_audio_config()
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
