from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import Voice, SynthesisRequest, SynthesisResponse


def synthesize_text(text: str, voice_name: str, language_code: str) -> bytes:
    """Synthesizes speech from the input string of text."""
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
