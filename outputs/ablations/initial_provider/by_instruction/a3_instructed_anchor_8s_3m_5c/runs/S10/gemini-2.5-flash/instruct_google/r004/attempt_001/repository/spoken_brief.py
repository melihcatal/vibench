import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> str:
    """
    Generates a spoken brief from text using Google Cloud Text-to-Speech API.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio output
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input, 
            "voice": voice, 
            "audio_config": audio_config
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath

