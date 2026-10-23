import os
import openai
from pydub import AudioSegment

# Provider: OpenAI TTS (Azure equivalent possible)
openai.api_key = os.getenv("OPENAI_API_KEY")

def reviewer_brief_audio(text: str, voice: str = 'alloy') -> bytes:
    """Generate spoken brief for reviewers using OpenAI's text-to-speech.

    Returns raw audio bytes.
    """
    tts_response = openai.Audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    # openai returns binary stream, read into bytes
    return tts_response.content
