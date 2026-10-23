import os
from speech_client import get_tts_client
from speech_models import SSMLRequest, AudioResponse


def synthesize_ssml(
    ssml_content: str,
    voice_id: str = "en-US-Neural2-J",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> bytes:
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    from google.cloud import texttospeech

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_content)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_id,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
