import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> None:
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

