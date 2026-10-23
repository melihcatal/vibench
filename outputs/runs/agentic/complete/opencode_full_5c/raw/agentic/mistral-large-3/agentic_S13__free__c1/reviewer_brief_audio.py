from typing import Dict
from gtts import gTTS
import os


def generate_reviewer_brief(text: str, output_file: str = "reviewer_brief.mp3") -> Dict:
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_file)
        return {"audio_file": output_file, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}
