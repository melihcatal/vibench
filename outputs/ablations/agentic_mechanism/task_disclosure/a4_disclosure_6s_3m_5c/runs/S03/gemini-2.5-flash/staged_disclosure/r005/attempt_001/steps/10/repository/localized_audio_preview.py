
from google.cloud import texttospeech

def generate_audio_preview(text, language_code, output_filename):
    """Generates an audio preview of the given text in the specified language."""
    client = texttospeech.TextToSpeechClient() # Google Cloud Text-to-Speech client

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice type (e.g., Wavenet, Standard) and language
    # You can customize these parameters based on available voices for the language
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the audio file type
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
    # Set your Google Cloud credentials before running this (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more information, visit: https://cloud.google.com/docs/authentication/getting-started
    
    # Example 1: English
    generate_audio_preview("Hello, this is a spoken preview of the English translation.", "en-US", "english_preview.mp3")

    # Example 2: Spanish
    generate_audio_preview("Hola, esta es una vista previa hablada de la traducción al español.", "es-ES", "spanish_preview.mp3")

    # Example 3: French
    generate_audio_preview("Bonjour, ceci est un aperçu vocal de la traduction française.", "fr-FR", "french_preview.mp3")
