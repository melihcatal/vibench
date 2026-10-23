import os
from google.cloud import texttospeech


def generate_brief_audio(text: str, output_filepath: str = "output.mp3") -> str:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
