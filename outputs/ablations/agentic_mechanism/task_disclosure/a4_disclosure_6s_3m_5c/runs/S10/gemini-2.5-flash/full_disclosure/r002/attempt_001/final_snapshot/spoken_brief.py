
from google.cloud import texttospeech
import os

def generate_spoken_brief(text: str, output_filename: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.

    Args:
        text: The text content to be converted into speech.
        output_filename: The name of the output audio file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, you might set it like:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice to be used
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example: a standard US English Wavenet voice
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
