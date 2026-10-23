from google.cloud import texttospeech
from typing import Optional


def generate_reviewer_brief_audio(text: str, output_file: str) -> Optional[str]:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    
    return output_file