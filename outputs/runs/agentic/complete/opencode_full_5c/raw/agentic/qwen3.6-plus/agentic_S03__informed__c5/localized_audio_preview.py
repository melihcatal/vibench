import os
import base64
import tempfile
from typing import Optional
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient
from translation_models import (
    LocalizedAudioPreviewRequest,
    LocalizedAudioPreviewResponse,
)

ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
ELEVENLABS_DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_MODEL = "eleven_multilingual_v2"


def _get_elevenlabs_client() -> ElevenLabs:
    api_key = os.environ.get(ELEVENLABS_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"ElevenLabs API key not found. Set the {ELEVENLABS_API_KEY_ENV} environment variable."
        )
    return ElevenLabs(api_key=api_key)


def _estimate_audio_duration(text: str, words_per_minute: int = 150) -> float:
    word_count = len(text.split())
    return (word_count / words_per_minute) * 60.0


def generate_audio_preview(
    request: LocalizedAudioPreviewRequest,
) -> LocalizedAudioPreviewResponse:
    client = _get_elevenlabs_client()

    voice_id = request.voice_id or ELEVENLABS_DEFAULT_VOICE

    audio_generator = client.generate(
        text=request.text,
        voice=voice_id,
        model=ELEVENLABS_MODEL,
    )

    audio_bytes = b"".join(audio_generator)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_url = f"data:audio/mpeg;base64,{audio_base64}"

    duration = _estimate_audio_duration(request.text)

    return LocalizedAudioPreviewResponse(
        audio_url=audio_url,
        duration_seconds=round(duration, 2),
        voice_id=voice_id,
    )


def generate_audio_preview_to_file(
    request: LocalizedAudioPreviewRequest,
    output_path: Optional[str] = None,
) -> LocalizedAudioPreviewResponse:
    client = _get_elevenlabs_client()

    voice_id = request.voice_id or ELEVENLABS_DEFAULT_VOICE

    audio_generator = client.generate(
        text=request.text,
        voice=voice_id,
        model=ELEVENLABS_MODEL,
    )

    audio_bytes = b"".join(audio_generator)

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    duration = _estimate_audio_duration(request.text)

    return LocalizedAudioPreviewResponse(
        audio_url=f"file://{output_path}",
        duration_seconds=round(duration, 2),
        voice_id=voice_id,
    )


if __name__ == "__main__":
    req = LocalizedAudioPreviewRequest(
        text="Bonjour le monde, comment allez-vous?",
        target_lang="fr",
    )
    resp = generate_audio_preview(req)
    print(f"Audio URL: {resp.audio_url[:50]}...")
    print(f"Duration: {resp.duration_seconds}s")
    print(f"Voice: {resp.voice_id}")
