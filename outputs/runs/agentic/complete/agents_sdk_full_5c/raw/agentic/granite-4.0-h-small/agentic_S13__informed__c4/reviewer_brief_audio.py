import os
import json
from typing import Dict
from safety_models import ModerationResponse, CategoryScore, UnsafeSpan
# Use ElevenLabs Text-to-Speech API as concrete provider
import elevenlabs
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
elevenlabs.api_key = ELEVENLABS_API_KEY

def generate_speech(text: str, speaker='jenny') -> Dict[str, str]:
    """Generates a spoken brief for moderation reviewers using ElevenLabs TTS."""
    speech = elevenlabs.TextToSpeech().generate_speech(
        text=text,
        voice_name=speaker,
        format='mp3'
    ).audio_content
    # Speech SDK returns bytes; store as base64 string for simplicity
    import base64
    audio_b64 = base64.b64encode(speech).decode('utf-8')
    return {'audio_base64': audio_b64}
