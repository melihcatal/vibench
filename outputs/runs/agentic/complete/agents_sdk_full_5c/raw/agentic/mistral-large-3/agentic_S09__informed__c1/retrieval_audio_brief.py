import os
from typing import List
from google.cloud import texttospeech_v1 as tts


def generate_audio_brief(texts: List[str], output_file: str) -> None:
    """Generate a spoken brief from retrieved search results using Google Cloud Text-to-Speech."""
    client = tts.TextToSpeechClient()
    
    combined_text = " \n".join(texts)
    synthesis_input = tts.SynthesisInput(text=combined_text)
    
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"
    )
    
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open(output_file, "wb") as out:
        out.write(response.audio_content)