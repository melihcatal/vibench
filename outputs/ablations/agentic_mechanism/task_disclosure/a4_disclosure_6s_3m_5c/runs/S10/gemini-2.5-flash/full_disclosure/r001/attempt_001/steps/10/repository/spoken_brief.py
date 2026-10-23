
import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text: The input text to be converted to speech.
        output_filepath: The path to save the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
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

    # Write the response audio content to the output file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

