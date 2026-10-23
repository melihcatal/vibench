import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def platform_brief_audio(prompt: str) -> bytes:
    """Generate a short spoken briefing from the platform model output using TTS."""
    # Azure AI Speech Text-to-Speech as example
    endpoint = os.getenv("AZURE_SPEECH_TTS_ENDPOINT")
    key = os.getenv("AZURE_SPEECH_TTS_KEY")
    if not endpoint or not key:
        raise RuntimeError("Speech TTS credentials not configured")

    import requests
    url = f"{endpoint}/cognitiveservices/v1"
    headers = {
        "Authorization": f"Bearer {key}",
        "User-Agent": "speech-sdk-python",
        "X-Search-AppId": "SpeechService",
        "X-Search-ClientVersion": "1.0.0",
        "Content-Type": "application/ssml+xml",
    }
    ssml = f"<speak version='1.0' xml:lang='en-US'><voice name='en-US-AriaNeural'>{prompt}</voice></speak>"
    payload = {
        "Input": {
            "Format": "Riff24Khz16BitMonoPcm",
            "Text": ssml,
            "VoiceName": "en-US-AriaNeural",
        },
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    # Assuming audio returned as base64 in resp.json()['Audio']
    audio_base64 = resp.json().get("Audio")
    if not audio_base64:
        raise ValueError("No audio returned from TTS service")
    import base64
    return base64.b64decode(audio_base64)


if __name__ == "__main__":
    # Example usage
    AZURE_SPEECH_TTS_ENDPOINT = os.getenv("AZURE_SPEECH_TTS_ENDPOINT")
    AZURE_SPEECH_TTS_KEY = os.getenv("AZURE_SPEECH_TTS_KEY")
    prompt = "Welcome to the daily briefing."
    audio_bytes = platform_brief_audio(prompt)
    # Save to file for verification
    with open("briefing.wav", "wb") as f:
        f.write(audio_bytes)
    print("Briefing audio written to briefing.wav")