import os
from google.cloud import texttospeech_v1 as texttospeech


def generate_audio_briefing(text: str, output_filepath: str) -> str:
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set."
        )

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection for US English with a standard male voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
