from google.cloud import texttospeech
import os


def generate_audio_brief(text: str, output_filepath: str = "output.mp3") -> str:
    """Generates a spoken audio brief from text using Google Cloud Text-to-Speech.

    Args:
        text: The text string to convert to speech.
        output_filepath: The path to save the generated audio file. Default is "output.mp3".

    Returns:
        The path to the generated audio file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # For local development, this usually points to a service account key file.
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
            "Text-to-Speech might fail without proper authentication."
        )

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Or MALE/FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
