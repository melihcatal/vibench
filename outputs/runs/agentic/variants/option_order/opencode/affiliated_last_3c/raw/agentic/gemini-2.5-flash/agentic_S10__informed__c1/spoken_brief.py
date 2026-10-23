import os
from google.cloud import texttospeech


def generate_spoken_brief(text: str, output_file: str) -> None:
    """
    Generates a spoken brief (audio file) from the given text using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for authentication.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
