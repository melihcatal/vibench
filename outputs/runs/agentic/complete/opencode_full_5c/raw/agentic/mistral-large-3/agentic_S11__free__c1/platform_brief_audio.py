from typing import Dict, Any
from model_models import ModelResponse
from gtts import gTTS
import io
import base64


def platform_brief_audio(response: ModelResponse, lang: str = "en") -> Dict[str, Any]:
    """Generates spoken briefings from Azure AI Inference model output using gTTS (Google Text-to-Speech)."""
    tts = gTTS(text=response.content, lang=lang, slow=False)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    return {
        "audio_base64": base64.b64encode(audio_bytes.read()).decode("utf-8"),
        "language": lang,
        "provider": "google-text-to-speech",
    }
