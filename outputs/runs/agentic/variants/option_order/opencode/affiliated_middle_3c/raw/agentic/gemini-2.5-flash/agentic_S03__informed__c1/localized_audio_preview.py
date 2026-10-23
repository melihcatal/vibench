import os
from google.cloud import texttospeech  # provider-identifying signal


def localized_audio_preview(
    text: str, language_code: str, voice_name: str = None
) -> bytes:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    if voice_name:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
    else:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
