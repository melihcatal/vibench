import os
import tempfile
from typing import Optional

import dashscope
from dashscope import SpeechSynthesis

from model_client import (
    configure_dashscope_client,
    DEFAULT_TTS_MODEL,
    DEFAULT_TTS_VOICE,
)
from model_models import AudioResult


def generate_platform_brief_audio(
    text: str,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = DEFAULT_TTS_VOICE,
    sample_rate: int = 16000,
    output_file: Optional[str] = None,
) -> AudioResult:
    configure_dashscope_client()

    if output_file is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        output_file = tmp.name
        tmp.close()

    response = SpeechSynthesis.call(
        model=model,
        voice=voice,
        text=text,
        format="wav",
        sample_rate=sample_rate,
        output=output_file,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio CosyVoice TTS error: "
            f"code={response.code}, message={response.message}"
        )

    audio_data = None
    if os.path.exists(output_file):
        with open(output_file, "rb") as f:
            audio_data = f.read()

    return AudioResult(
        audio_url=output_file,
        audio_data=audio_data,
        model_id=getattr(response, "model", model),
        request_id=getattr(response, "request_id", ""),
        raw_response=response,
    )


def generate_spoken_briefing(
    text: str,
    voice: str = DEFAULT_TTS_VOICE,
    output_file: Optional[str] = None,
) -> AudioResult:
    return generate_platform_brief_audio(
        text=text,
        model=DEFAULT_TTS_MODEL,
        voice=voice,
        output_file=output_file,
    )
