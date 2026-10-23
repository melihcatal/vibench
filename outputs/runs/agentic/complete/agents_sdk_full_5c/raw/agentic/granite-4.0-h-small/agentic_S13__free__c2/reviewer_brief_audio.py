import os
from safety_client import safety_client
from safety_models import SafetyModels
from gtts_client import gTTS # pip install gtts
import tempfile

def reviewer_brief_audio(brief_text: str, output_path: str = 'brief.mp3') -> None:
    """Generate a spoken brief for moderation reviewers using a hosted TTS service (Google Text‑to‑Speech)."""
    # Google Cloud Text‑to‑Speech client (concrete integration)
    from google.cloud import texttospeech_v1 as texttospeech
    client = texttospeech.TextToSpeechClient()
    input_synth = texttospeech.SynthesisInput(text=brief_text)
    # Choose a WaveNet voice for a natural brief
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name='en-US-Wavenet-D'
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(input=input_synth, voice=voice, audio_config=audio_config)
    with open(output_path, 'wb') as out_file:
        out_file.write(response.audio_content)
