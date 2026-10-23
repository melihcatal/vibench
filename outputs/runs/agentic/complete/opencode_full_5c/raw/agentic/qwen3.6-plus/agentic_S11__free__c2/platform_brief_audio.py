from model_client import create_openai_client, OPENAI_API_BASE
from model_models import AudioResult


SUPPORTED_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_platform_brief_audio(
    text: str,
    voice: str = "nova",
    model: str = "tts-1",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> AudioResult:
    if voice not in SUPPORTED_TTS_VOICES:
        raise ValueError(
            f"OpenAI TTS voice '{voice}' is not supported. Choose from: {SUPPORTED_TTS_VOICES}"
        )
    client = create_openai_client(base_url=OPENAI_API_BASE)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )
    audio_bytes = response.content
    return AudioResult(
        audio_bytes=audio_bytes,
        model=model,
        format=response_format,
        raw_result=response,
    )


def generate_platform_brief_audio_hd(
    text: str,
    voice: str = "nova",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> AudioResult:
    return generate_platform_brief_audio(
        text=text,
        voice=voice,
        model="tts-1-hd",
        response_format=response_format,
        speed=speed,
    )
