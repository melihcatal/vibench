from typing import Dict, Any
import os
from model_client import LLMClient
from model_models import LLMRequest


async def generate_spoken_brief(text: str, voice: str = "alloy") -> Dict[str, Any]:
    """Generate a spoken brief from model output using ElevenLabs TTS API."""
    client = LLMClient()
    prompt = (
        f"Convert the following text into a concise spoken brief. "
        f"The output should be natural and engaging for audio delivery.\n\n"
        f"Text: {text}\n\n"
        f"Spoken Brief:"
    )
    request = LLMRequest(prompt=prompt, max_tokens=500)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    spoken_text = response["choices"][0]["message"]["content"]
    await client.close()

    # Use ElevenLabs TTS API to generate audio
    tts_api_key = os.getenv("ELEVENLABS_API_KEY", "")
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        "xi-api-key": tts_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": spoken_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    import httpx

    async with httpx.AsyncClient() as tts_client:
        tts_response = await tts_client.post(tts_url, json=payload, headers=headers)
        tts_response.raise_for_status()

    return {
        "spoken_text": spoken_text,
        "audio_content": tts_response.content,
        "voice": voice,
    }
