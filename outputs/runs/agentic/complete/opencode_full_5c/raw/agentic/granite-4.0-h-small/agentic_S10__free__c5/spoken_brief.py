import os
import json
from model_client import HostedLLMClient


def generate_spoken_brief(output_text: str, voice_name: str = "alloy") -> str:
    """Creates a short spoken brief (audio URL) from model output using a TTS service.

    This demo uses OpenAI's audio generation endpoint (or a placeholder).
    Returns a public URL to the generated speech.
    """
    client = HostedLLMClient()
    payload = {
        "model": "tts-1",
        "voice": voice_name,
        "input": output_text,
        "response_format": "url",
    }
    response = client._request("/v1/audio/speech", payload)
    # The endpoint returns a direct URL to the audio file
    return response.get("url", "No URL returned")


if __name__ == "__main__":
    brief = "Today the weather is sunny and warm, perfect for a picnic."
    url = generate_spoken_brief(brief)
    print("Spoken brief URL:", url)
