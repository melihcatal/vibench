import os
from typing import List
from google.cloud import texttospeech_v1 as texttospeech


def generate_audio_brief(texts: List[str], output_file: str) -> None:
    client = texttospeech.TextToSpeechClient()

    combined_text = " \n".join(texts)
    synthesis_input = texttospeech.SynthesisInput(text=combined_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)