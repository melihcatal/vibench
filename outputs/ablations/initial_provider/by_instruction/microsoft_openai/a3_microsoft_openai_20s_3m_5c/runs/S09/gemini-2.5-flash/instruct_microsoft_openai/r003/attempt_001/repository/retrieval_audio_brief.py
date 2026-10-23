import os
from google.cloud import texttospeech
from typing import List, Dict

def generate_audio_brief(text: str, output_filepath: str) -> None:
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file {output_filepath}")