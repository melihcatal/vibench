import os
from speech_client import get_tts_client
from speech_models import TextToSpeechRequest, AudioResponse


def synthesize_text(
    text: str, voice_id: str = "en-US-Neural2-J", language_code: str = "en-US"
) -> bytes:
    """Synthesize plain text to audio byte stream using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    from google.cloud import texttospeech

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_id,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
