from google.cloud import texttospeech
import os


def generate_audio_preview(
    text: str, language_code: str, voice_name: str = None
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    if voice_name:
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
    else:
        # Select a default voice based on language code if not specified
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
