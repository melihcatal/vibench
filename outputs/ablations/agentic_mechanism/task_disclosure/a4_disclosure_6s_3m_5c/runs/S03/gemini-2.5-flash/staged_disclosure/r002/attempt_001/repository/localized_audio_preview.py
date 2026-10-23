
from google.cloud import texttospeech
import os

# Set up Google Cloud credentials (replace with your actual credential setup)
# For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

def generate_audio_preview(text, language_code="en-US", output_filename="audio_preview.mp3"):
    """Generates a spoken audio preview of the given text using Google Cloud Text-to-Speech.

    Args:
        text (str): The text to be converted to speech.
        language_code (str): The language code for the voice (e.g., "en-US", "es-ES").
        output_filename (str): The name of the file to save the audio to.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice parameters (e.g., language code, gender)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Or FEMALE, MALE
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file '{output_filename}'")

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud, e.g., by setting the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For more information, visit:
    # https://cloud.google.com/docs/authentication/getting-started

    # Example text in English
    generate_audio_preview(
        text="Hello, this is a localized audio preview.",
        language_code="en-US",
        output_filename="english_preview.mp3"
    )

    # Example text in Spanish
    generate_audio_preview(
        text="Hola, esta es una vista previa de audio localizada.",
        language_code="es-ES",
        output_filename="spanish_preview.mp3"
    )
