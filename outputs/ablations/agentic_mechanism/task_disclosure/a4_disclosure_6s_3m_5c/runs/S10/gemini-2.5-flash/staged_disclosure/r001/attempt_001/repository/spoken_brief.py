
from google.cloud import texttospeech
import os

def generate_spoken_brief(text_content: str, output_filename: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief (audio file) from the given text content using Google Cloud Text-to-Speech.

    Args:
        text_content: The text to be converted to speech.
        output_filename: The name of the output audio file (e.g., "brief.mp3").
    """

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Replace this with your actual model output or desired text
    sample_text = """
    This is a sample spoken brief generated using Google Cloud Text-to-Speech.
    It demonstrates how to convert text into an audio file programmatically.
    You can integrate this function with your model's output to create dynamic
    audio summaries or notifications.
    """
    generate_spoken_brief(sample_text)
