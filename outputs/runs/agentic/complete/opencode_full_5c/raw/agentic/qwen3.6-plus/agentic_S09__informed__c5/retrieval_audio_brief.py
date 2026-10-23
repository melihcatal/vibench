import os
from elevenlabs import ElevenLabs


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def generate_audio_brief(search_results, voice_id=None, model_id=None, api_key=None):
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    client = ElevenLabs(api_key=api_key)
    if isinstance(search_results, list):
        summary_text = " ".join(
            r.get("text", str(r)) if isinstance(r, dict) else str(r)
            for r in search_results
        )
    elif isinstance(search_results, dict):
        summary_text = search_results.get("summary", str(search_results))
    else:
        summary_text = str(search_results)
    voice = voice_id or DEFAULT_VOICE_ID
    model = model_id or DEFAULT_MODEL_ID
    audio = client.text_to_speech.convert(
        text=summary_text,
        voice_id=voice,
        model_id=model,
    )
    return audio
