import os
from elevenlabs import generate, set_api_key
from model_models import AudioBriefingResult

def generate_elevenlabs_audio(text: str, voice: str = "Rachael", model: str = "eleven_multilingual_v2") -> AudioBriefingResult:
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set.")

    set_api_key(api_key)

    audio = generate(text=text, voice=voice, model=model)

    return AudioBriefingResult(audio_content=audio, audio_format="mp3")
