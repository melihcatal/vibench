import os
from typing import List, Dict, Any
from google.cloud import texttospeech  # Google Cloud Text-to-Speech API


def generate_audio_brief(
    text_content: str, output_filepath: str = "audio_brief.mp3"
) -> Dict[str, str]:
    """Generates a spoken brief from text content using Google Cloud Text-to-Speech API.
    The audio brief is saved to the specified output_filepath.
    """
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Build the voice request, select the language code (e.g., "en-US") and the voice gender (e.g., "NEUTRAL")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return {
        "status": "Audio brief generated successfully",
        "filepath": os.path.abspath(output_filepath),
    }
