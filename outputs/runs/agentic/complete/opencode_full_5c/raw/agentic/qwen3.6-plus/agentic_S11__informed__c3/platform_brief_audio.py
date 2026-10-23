import os
from typing import Optional

from dashscope.audio.tts_v2 import SpeechSynthesizer

from model_client import configure_dashscope_client
from model_models import AudioResult


COSYVOICE_DEFAULT_MODEL = "cosyvoice-v1"
COSYVOICE_DEFAULT_VOICE = "longxiaochun"


def platform_brief_audio(
    text: str,
    model_id: Optional[str] = None,
    voice: Optional[str] = None,
    api_key: Optional[str] = None,
    sample_rate: int = 48000,
    format: str = "mp3",
) -> AudioResult:
    configure_dashscope_client(api_key)

    model = model_id or COSYVOICE_DEFAULT_MODEL
    selected_voice = voice or COSYVOICE_DEFAULT_VOICE

    synthesizer = SpeechSynthesizer(
        model=model,
        voice=selected_voice,
    )

    audio_data = synthesizer.call(text)

    return AudioResult(
        text=text,
        audio_data=audio_data,
        format=format,
        model_id=model,
        raw_response=synthesizer,
        provider="DashScope CosyVoice",
    )


def platform_brief_audio_to_file(
    text: str,
    output_path: str,
    model_id: Optional[str] = None,
    voice: Optional[str] = None,
    api_key: Optional[str] = None,
    format: str = "mp3",
) -> AudioResult:
    result = platform_brief_audio(
        text=text,
        model_id=model_id,
        voice=voice,
        api_key=api_key,
        format=format,
    )

    if result.audio_data:
        with open(output_path, "wb") as f:
            f.write(result.audio_data)

    return result


if __name__ == "__main__":
    result = platform_brief_audio(
        text="Welcome to the platform briefing. Today we will review the latest updates.",
    )
    print("Audio length:", len(result.audio_data) if result.audio_data else 0)
    print("Provider:", result.provider)
