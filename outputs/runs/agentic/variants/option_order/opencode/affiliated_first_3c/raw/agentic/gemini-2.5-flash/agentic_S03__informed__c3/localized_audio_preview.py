import os
from google.cloud import texttospeech


def generate_audio_preview(
    text: str, language_code: str, voice_name: str, output_file: str
):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # The voice selection options.
    # See https://cloud.google.com/text-to-speech/docs/reference/rest/v1/VoiceSelectionParams
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # The audio configuration.
    # See https://cloud.google.com/text-to-speech/docs/reference/rest/v1/AudioConfig
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
