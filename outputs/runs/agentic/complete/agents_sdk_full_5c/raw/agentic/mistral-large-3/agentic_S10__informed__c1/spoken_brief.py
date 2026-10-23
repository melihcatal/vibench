import os
from typing import Optional
from google.cloud import texttospeech_v1 as tts


def generate_spoken_brief(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Wavenet-D",
    output_file: Optional[str] = None
) -> bytes:
    """
    Generate a spoken brief from the model output using Google Cloud Text-to-Speech.
    """
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    if output_file:
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

    return response.audio_content