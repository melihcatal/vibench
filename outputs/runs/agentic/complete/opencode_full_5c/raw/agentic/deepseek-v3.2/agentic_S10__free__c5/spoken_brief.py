import os
from openai import OpenAI
from model_models import SpeechRequest, SpeechResponse


def generate_spoken_brief(
    text: str, voice: str = "alloy", speed: float = 1.0
) -> SpeechResponse:
    """Generate a spoken brief from the model output using OpenAI TTS."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice not in valid_voices:
        voice = "alloy"

    try:
        response = client.audio.speech.create(
            model="tts-1", voice=voice, input=text, speed=speed
        )

        audio_data = response.content

        return SpeechResponse(
            audio_data=audio_data,
            format="mp3",
            duration_seconds=len(audio_data) / 16000,  # Approximate duration
            provider="openai",
        )
    except Exception as e:
        raise Exception(f"Failed to generate speech: {str(e)}")
