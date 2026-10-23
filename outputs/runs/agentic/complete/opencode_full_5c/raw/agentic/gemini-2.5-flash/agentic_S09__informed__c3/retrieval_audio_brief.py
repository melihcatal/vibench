import os
from google.cloud import texttospeech


def generate_audio_brief(text: str, output_filepath: str):
    """
    Generates a spoken audio brief from retrieved search results using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for authentication.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filepath}"')
