import asyncio
import openai
from model_models import NormalizedResponse

OPENAI_VOICE_MODEL = "tts-1-hd"  # concrete voice model identifier

def platform_brief_audio(text: str, voice: str = "alloy") -> str:
    """
    Generate a spoken briefing (audio) from platform model output using OpenAI's TTS API.
    Returns a temporary URL to the generated audio file.
    """
    print(f"Generating audio with voice '{voice}' and model '{OPENAI_VOICE_MODEL}'...")
    response = openai.Audio.synthesize(
        model=OPENAI_VOICE_MODEL,
        voice=voice,
        input=text
    )
    # The TTS endpoint returns a presigned URL to the audio file
    audio_url = response["audio_url"]
    return audio_url

# Example usage for local testing
if __name__ == "__main__":
    from model_client import ManagedModelClient
    client = ManagedModelClient()
    deployment = os.getenv("DEPLOYMENT_ID")
    txt = "Welcome to the weather briefing. Today is sunny."
    resp = client.invoke_model(deployment, txt, stream=False)
    norm = NormalizedResponse.from_openai(resp)
    # Use generated_text as the briefing script
    audio_url = platform_brief_audio(norm.data["generated_text"])  # type: ignore
    print("Audio URL:", audio_url)

# Note: For actual deployment, handle credentials via OPENAI_API_KEY env var.
