import os
import requests

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # concrete voice: Rachel
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def generate_spoken_brief(text: str, output_path: str = "spoken_brief.mp3") -> str:
    \"\"\"Generate TTS audio brief from model output using ElevenLabs.\"\"\"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text[:5000],  # truncate if too long
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(TTS_URL, json=data, headers=headers)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path