from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import get_default_voice_params, get_default_audio_config

def synthesize_text(text: str) -> bytes:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = get_default_voice_params()
    audio_config = get_default_audio_config()

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content
