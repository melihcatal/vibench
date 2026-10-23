import os
from openai import OpenAI

from safety_client import get_openai_client
from safety_models import AudioBriefInput, AudioBriefOutput

def generate_reviewer_brief_audio(audio_input: AudioBriefInput) -> AudioBriefOutput:
    client = get_openai_client()

    try:
        # OpenAI Text-to-Speech API call
        response = client.audio.speech.create(
            model="tts-1",  # Concrete model identifier
            voice="alloy",  # A standard voice
            input=audio_input.text,
        )
        
        # The response.content is a byte stream
        audio_content = response.content
        return AudioBriefOutput(audio_content=audio_content)
    except Exception as e:
        print(f"Error generating audio brief with OpenAI TTS: {e}")
        return AudioBriefOutput(audio_content=b'')
