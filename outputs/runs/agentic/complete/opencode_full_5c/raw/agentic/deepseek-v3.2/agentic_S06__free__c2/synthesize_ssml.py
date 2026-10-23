import os
from google.cloud import texttospeech


def synthesize_ssml(
    ssml_text,
    voice_name="en-US-Neural2-J",
    speaking_rate=1.0,
    pitch=0.0,
    volume_gain_db=0.0,
):
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
