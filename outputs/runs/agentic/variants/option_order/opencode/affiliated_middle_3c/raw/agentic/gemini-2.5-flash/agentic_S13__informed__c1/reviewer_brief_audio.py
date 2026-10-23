import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(text: str, output_filepath: str) -> None:
    # Google Cloud Text-to-Speech uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure this environment variable is set to the path of your service account key file.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    # Using a standard Google Cloud Text-to-Speech voice, for example, "en-US-Wavenet-D"
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
