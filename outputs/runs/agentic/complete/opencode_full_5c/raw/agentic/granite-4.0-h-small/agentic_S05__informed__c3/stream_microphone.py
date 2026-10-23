import asyncio
from typing import AsyncGenerator

# DashScope Real-time ASR integration
# SDK: dashscope
# Service: DashScope Real-time speech recognition

# Configuration (set env vars before running)
# export DASHSCOPE_API_KEY="your-dashscope-key"


async def stream_microphone() -> AsyncGenerator[str, None]:
    """Yield interim transcripts from live microphone audio using DashScope streaming ASR."""
    import dashscope
    import pyaudio

    client = dashscope.speech.SpeechRecognizer(
        api_key="${DASHSCOPE_API_KEY}", model="general"
    )

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    async def _send_audio():
        while True:
            data = stream.read(1024)
            if not data:
                break
            response = client.stt(
                audio=data,
                sample_rate=16000,
                recognize_config={"model": "general", "enable_interim_results": True},
            )
            yield response.get("transcript", "")

    async for transcript in _send_audio():
        yield transcript


if __name__ == "__main__":
    async for t in stream_microphone():
        print("Interim:", t)
