from google.cloud import texttospeech
import os

def generate_spoken_preview(text: str, language_code: str, output_filename: str = "output.mp3"):
    """
    Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.

    Args:
        text: The translated text to convert to speech.
        language_code: The BCP-47 language code for the voice (e.g., "en-US", "es-ES").
        output_filename: The name of the file to save the audio to.
    """

    # Set up Google Cloud credentials (assuming GOOGLE_APPLICATION_CREDENTIALS environment variable is set)
    # This is a provider-identifying signal.
    client = texttospeech.TextToSpeechClient()

    # Set the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice.
    # We are using a standard voice, which is identifiable with its language_code and ssml_gender.
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

    # The audio content is streamable and can be saved to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
