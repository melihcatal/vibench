from google.cloud import texttospeech
from speech_client import get_speech_client
from speech_models import VoiceSelectionParams, AudioConfig


def synthesize_text(
    text: str, voice_params: VoiceSelectionParams, audio_config: AudioConfig
) -> bytes:
    """Synthesizes plain text into audio."""
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_params.language_code,
        name=voice_params.name,
    )

    gcp_audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[audio_config.audio_encoding]
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=gcp_audio_config
    )

    return response.audio_content
