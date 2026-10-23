import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationMetadata

def platform_brief_audio(model_output: str, voice_id: str = "alloy") -> bytes:
    """
    Synthesize spoken audio from model output using a provider TTS service.
    Uses Azure AI Speech Text-to-Speech (replaceable with Google Cloud TTS, ElevenLabs, etc.).
    Returns raw PCM/OGG audio bytes suitable for downstream storage or streaming.
    """
    client = ManagedModelClient()
    endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
    key = os.getenv("AZURE_SPEECH_KEY")
    if not (endpoint and key):
        raise RuntimeError("Azure Speech credentials not configured")
    import requests
    resp = requests.post(
        f"{endpoint}/cognitiveservices/v1?api-version=1.0",
        json={
            "Text": model_output,
            "VoiceName": voice_id,
            "OutputFormat": "riff-16khz-16bit-mono-pcm",
        },
        headers={"Ocp-Apim-Subscription-Key": key},
    )
    resp.raise_for_status()
    return resp.content  # bytes of the audio file

# Minimal demo (uncomment to run)
# if __name__ == "__main__":
#     text = "Welcome to the AI brief service."
#     audio_bytes = platform_brief_audio(text)
#     with open("brief.wav", "wb") as f:
#         f.write(audio_bytes)
#     print("Audio written to brief.wav")
