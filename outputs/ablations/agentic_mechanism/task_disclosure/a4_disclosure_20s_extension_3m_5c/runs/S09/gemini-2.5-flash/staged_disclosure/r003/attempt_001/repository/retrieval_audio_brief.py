
import os
from google.cloud import texttospeech

def generate_audio_brief(text_content, output_filename="audio_brief.mp3"):
    """
    Generates a spoken brief from the given text content using Google Cloud Text-to-Speech.

    Args:
        text_content (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file (e.g., "audio_brief.mp3").
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
    # Ensure you have authenticated with Google Cloud, e.g., by setting the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For local development, you can set:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    sample_text = """
    This is a sample audio brief generated from search results.
    It provides a concise summary of the retrieved information.
    """
    generate_audio_brief(sample_text)
