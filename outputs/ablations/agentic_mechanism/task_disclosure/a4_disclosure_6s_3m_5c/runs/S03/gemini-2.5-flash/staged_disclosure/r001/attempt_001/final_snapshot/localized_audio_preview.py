from google.cloud import texttospeech
import os

def generate_localized_audio_preview(text: str, language_code: str, output_filename: str):
    """Generates spoken previews of translated copy using Google Cloud Text-to-Speech.

    Args:
        text: The text to be converted to speech.
        language_code: The BCP-47 language code (e.g., "en-US", "es-ES", "fr-FR").
        output_filename: The name of the file to save the audio to (e.g., "preview.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice gender (optional)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filename}'")

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    # For English
    generate_localized_audio_preview(
        text="Hello, this is an English audio preview.",
        language_code="en-US",
        output_filename="english_preview.mp3"
    )

    # For Spanish
    generate_localized_audio_preview(
        text="Hola, esta es una vista previa de audio en español.",
        language_code="es-ES",
        output_filename="spanish_preview.mp3"
    )

    # For French
    generate_localized_audio_preview(
        text="Bonjour, ceci est un aperçu audio en français.",
        language_code="fr-FR",
        output_filename="french_preview.mp3"
    )
