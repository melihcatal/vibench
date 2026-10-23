import os
from pydantic import BaseModel
from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse
from gtts import gTTS
import tempfile

class AudioBriefConfig(BaseModel):
    text: str = ""
    output_path: str = "output.mp3"
    lang: str = "en"


def generate_audio_brief(config: AudioBriefConfig) -> str:
    """Take model output text and synthesize an audio briefing using gTTS."""
    tts = gTTS(text=config.text, lang=config.lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(tts.read())
        audio_path = tmp.name
    print(f"Audio brief saved to {audio_path}")
    return audio_path

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are helpful.", "user": "Give a 30‑second briefing on renewable energy."},
                            config={"provider": "anthropic"})
    client = ManagedModelClient(provider=demo_req.config["provider"], api_key=os.getenv(demo_req.config["provider"] + "_API_KEY"))
    raw = client.chat(compute(demo_req.dict()))
    audio_path = generate_audio_brief(AudioBriefConfig(text=raw.get("output", ""), lang="en"))
    print(json.dumps({"audio_file": audio_path}, indent=2))
