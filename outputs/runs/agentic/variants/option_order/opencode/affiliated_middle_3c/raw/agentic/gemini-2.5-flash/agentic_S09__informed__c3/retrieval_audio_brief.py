import os
from google.cloud import texttospeech
from typing import List


def generate_spoken_brief(
    text_brief: str, output_audio_path: str = "output.mp3"
) -> str:
    # Google Cloud Text-to-Speech automatically uses GOOGLE_APPLICATION_CREDENTIALS
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

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

    # The response's audio_content is binary. Write it to a file.
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_audio_path}" ')

    return output_audio_path
