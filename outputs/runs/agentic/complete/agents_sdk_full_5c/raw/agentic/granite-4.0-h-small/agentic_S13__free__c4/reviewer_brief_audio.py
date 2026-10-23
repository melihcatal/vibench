# reviewer_brief_audio.py
"""Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
"""
import os
from google.cloud import texttospeech
from safety_models import SafetyResponse

def generate_audio_brief(rationale: str, output_path: str = "moderation_brief.wav") -> None:
    """Create a WAV file containing a spoken moderation rationale for reviewers.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to a service account JSON.
    """
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=rationale)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio brief written to {output_path}")
