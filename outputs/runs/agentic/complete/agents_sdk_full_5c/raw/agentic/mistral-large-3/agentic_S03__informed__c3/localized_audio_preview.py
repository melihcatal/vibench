import os
from typing import List
from elevenlabs import generate, set_api_key
from translation_models import BatchTranslationResponse

set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def localized_audio_preview(texts: List[str], voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> List[bytes]:
    audio_previews = []
    for text in texts:
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        audio_previews.append(audio)
    return audio_previews