import os
from typing import Dict, Any
from google.cloud import texttospeech_v1 as texttospeech


def generate_reviewer_brief(text: str, language_code: str = "en-US") -> bytes:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS."
        )

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
    except Exception as e:
        raise Exception(f"Google Cloud Text-to-Speech failed: {str(e)}")
