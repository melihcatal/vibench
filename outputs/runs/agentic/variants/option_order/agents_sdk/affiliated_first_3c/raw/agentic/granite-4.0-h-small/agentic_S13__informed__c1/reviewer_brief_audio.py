# [LATER-STEP] reviewer_brief_audio.py

from google.cloud import texttospeech
import os

# Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech
# (scorable provider)

def generate_audio_brief(approval_decision: str, unsafe_categories: list) -> bytes:
    """Creates an audio file (MP3) summarizing the moderation decision.

    Returns raw bytes of the synthesized speech.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=approval_decision)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-L",  # female US English
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
