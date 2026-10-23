import json
from model_models import ModelInvocationResponse
from typing import Dict
import os
# Use ElevenLabs Text-to-Speech (TTS) service for spoken briefings.
import elevenlabs

def platform_brief_audio(raw_response: ModelInvocationResponse) -> Dict[str, Any]:
    """
    Generate a spoken audio file (URL) from the model output using ElevenLabs.
    Returns a dict with the original text and a downloadable audio URL.
    """
    # ElevenLabs client configured from env variable ELEVENLABS_API_KEY
    client = elevenlabs.Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
    try:
        synthesis = client.text_to_speech(
            text=raw_response.text,
            voice="e0a0c0b3-5e7d-4c0a-9d7c-8c2f6e2f6e3f"  # default English voice; replace as needed
        )
        # The API returns a URL to the audio file.
        audio_url = synthesis["audio_url"]
    except Exception as exc:
        return {
            "text": raw_response.text,
            "audio_url": None,
            "status": "error",
            "error_message": str(exc)
        }
    return {
        "text": raw_response.text,
        "audio_url": audio_url,
        "audio_format": "mp3",
        "service": "elevenlabs"
    }

# Simple test harness
if __name__ == "__main__":
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("DEPLOYMENT_ID must be set.")
    prompt = "Welcome to your daily brief summary."
    response = collect_platform_metadata(deployment, prompt)
    audio_info = platform_brief_audio(response)
    print(json.dumps(audio_info, indent=2))
