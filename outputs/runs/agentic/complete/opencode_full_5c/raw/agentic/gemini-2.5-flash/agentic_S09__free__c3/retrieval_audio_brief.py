import os
from google.cloud import texttospeech


def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    """Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        ),
        audio_config=audio_config,
    )

    # The response's audio_content is binary. Write it to an output file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
