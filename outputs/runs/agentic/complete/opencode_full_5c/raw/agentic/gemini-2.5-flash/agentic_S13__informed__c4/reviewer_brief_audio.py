import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(
    text: str, output_filepath: str = "reviewer_brief.mp3"
) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment.
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable is the provider-identifying signal.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice type and audio file type
    # Using a standard voice for simplicity, e.g., 'en-US-Wavenet-D' or 'en-US-Standard-D'
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-D",  # Provider-specific voice name
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an output file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
