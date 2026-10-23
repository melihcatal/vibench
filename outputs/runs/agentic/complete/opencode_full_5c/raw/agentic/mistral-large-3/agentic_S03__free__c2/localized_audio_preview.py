from typing import List
from google.cloud import texttospeech_v1
import os


def generate_spoken_preview(texts: List[str], language_code: str) -> List[bytes]:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech API."""
    client = texttospeech_v1.TextToSpeechClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    audio_contents = []
    for text in texts:
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        audio_contents.append(response.audio_content)

    return audio_contents
