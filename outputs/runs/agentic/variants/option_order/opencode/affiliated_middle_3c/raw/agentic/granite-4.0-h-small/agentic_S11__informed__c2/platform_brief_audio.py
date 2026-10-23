import os
import io
from pydub import AudioSegment
from pydub.playback import play
from model_client import ManagedModelClient
from model_models import InferenceResponse
from select_platform_resource import select_provider
from platform_output_embedding import embed_text


def generate_audio_brief(text: str, locale: str = "en") -> bytes:
    """Generate a spoken audio brief from model output using provider TTS."""
    # Use embedding provider TTS for demonstration (dashscope provides CosyVoice TTS)
    # For production, replace with Azure TTS, ElevenLabs, etc.
    if locale == "en":
        voice = "alloy"
    elif locale == "es":
        voice = "ladys_voice"
    else:
        voice = "alloy"
    # Call DashScope TTS SDK (requires DASHSCOPE_API_KEY)
    from dashscope import TextToSpeechClient

    tts_client = TextToSpeechClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
    resp = tts_client.synthesize(text=text, voice=voice)
    audio_bytes = io.BytesIO(resp["audio"])
    return audio_bytes.read()


def platform_brief_audio(provider: str, response: InferenceResponse) -> bytes:
    """Wrap embedding with raw provider response."""
    brief_text = response["text"]  # could be shortened/summarized here
    return generate_audio_brief(brief_text)


def main():
    config = {"provider": "dashscope", "model_id": "your-model-id"}
    client = ManagedModelClient(config)
    response = client.invoke({"prompt": "Welcome to the daily news briefing."})
    audio = platform_brief_audio(config["provider"], response)
    with open("brief.mp3", "wb") as f:
        f.write(audio)
    print("Audio brief saved as brief.mp3")


if __name__ == "__main__":
    main()
