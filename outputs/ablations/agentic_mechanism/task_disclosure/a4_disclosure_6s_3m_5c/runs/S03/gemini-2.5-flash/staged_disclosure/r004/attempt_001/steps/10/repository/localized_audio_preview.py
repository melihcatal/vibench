from google.cloud import texttospeech
import os

def generate_spoken_preview(text: str, language_code: str, output_filename: str):
    """Generates spoken audio from text using Google Cloud Text-to-Speech.

    Args:
        text: The text to be converted to speech.
        language_code: The BCP-47 language code (e.g., "en-US", "es-ES", "fr-FR").
        output_filename: The name of the file to save the audio to (e.g., "preview.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    # Example 1: English preview
    generate_spoken_preview(
        text="Hello, this is a localized audio preview in English.",
        language_code="en-US",
        output_filename="en_preview.mp3"
    )

    # Example 2: Spanish preview
    generate_spoken_preview(
        text="Hola, esto es una previsualización de audio localizada en español.",
        language_code="es-ES",
        output_filename="es_preview.mp3"
    )

    # Example 3: French preview
    generate_spoken_preview(
        text="Bonjour, ceci est un aperçu audio localisé en français.",
        language_code="fr-FR",
        output_filename="fr_preview.mp3"
    )
