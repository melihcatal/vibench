import os
from google.cloud import texttospeech


def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    """Generates a spoken brief from text using Google Cloud Text-to-Speech.
    The audio is saved to the specified output_filepath.
    """
    # Google Cloud Text-to-Speech typically uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure your environment is set up with these credentials.
    # For this example, we assume the credentials are implicitly available or configured.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
