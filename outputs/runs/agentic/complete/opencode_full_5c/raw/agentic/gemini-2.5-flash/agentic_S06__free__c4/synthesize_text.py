from speech_client import get_tts_client
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig
from google.cloud import texttospeech


def synthesize_text(
    text: str, voice_name: str, language_code: str, audio_encoding: str = "MP3"
) -> bytes:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding)
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content
