
import os
from google.cloud import texttospeech

def generate_localized_audio_preview(text: str, language_code: str, output_filename: str):
    """
    Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.

    Args:
        text (str): The text to synthesize.
        language_code (str): The language code for the voice (e.g., "en-US", "es-ES", "fr-FR").
        output_filename (str): The name of the output audio file (e.g., "preview.mp3").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code and a SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == '__main__':
    # Example usage:
    # Make sure to set up Google Cloud credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more information: https://cloud.google.com/docs/authentication/getting-started

    # English preview
    generate_localized_audio_preview(
        "Hello, this is a preview of the English translation.",
        "en-US",
        "en_preview.mp3"
    )

    # Spanish preview
    generate_localized_audio_preview(
        "Hola, esta es una vista previa de la traducción al español.",
        "es-ES",
        "es_preview.mp3"
    )

    # French preview
    generate_localized_audio_preview(
        "Bonjour, ceci est un aperçu de la traduction française.",
        "fr-FR",
        "fr_preview.mp3"
    )
