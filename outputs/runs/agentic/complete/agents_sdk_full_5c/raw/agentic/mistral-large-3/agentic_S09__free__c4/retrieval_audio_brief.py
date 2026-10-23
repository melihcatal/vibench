import os
from typing import List, Dict
from gtts import gTTS
import io
import base64

def generate_audio_brief(search_results: List[Dict[str, Any]], output_format: str = "mp3") -> str:
    brief_text = "Here are the top results: " + ". ".join(
        [f"Result {i + 1}: {result.get('text', '')}" for i, result in enumerate(search_results)]
    )
    tts = gTTS(text=brief_text, lang="en", slow=False)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return base64.b64encode(audio_buffer.read()).decode("utf-8")