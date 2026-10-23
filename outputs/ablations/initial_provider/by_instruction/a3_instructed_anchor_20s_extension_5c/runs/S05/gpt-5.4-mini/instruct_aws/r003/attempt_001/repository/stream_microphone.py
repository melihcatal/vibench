from typing import Iterator, Optional

from speech_client import load_speech_config, make_transcribe_streaming_client
from speech_models import TranscriptChunk


def microphone_audio_stream() -> Iterator[bytes]:
    try:
        import pyaudio
    except Exception as exc:
        raise RuntimeError("pyaudio is required for microphone streaming") from exc
    config = load_speech_config()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=config.media_sample_rate_hz, input=True, frames_per_buffer=1024)
    try:
        while True:
            yield stream.read(1024, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone(language_code: Optional[str] = None) -> Iterator[TranscriptChunk]:
    config = load_speech_config(language_code=language_code)
    client = make_transcribe_streaming_client(config.region_name)
    response = client.start_stream_transcription(
        LanguageCode=config.language_code,
        MediaSampleRateHertz=config.media_sample_rate_hz,
        MediaEncoding=config.media_encoding,
        AudioStream=(
            {"AudioEvent": {"AudioChunk": chunk}}
            for chunk in microphone_audio_stream()
        ),
    )
    for event in response["TranscriptResultStream"]:
        results = event.get("TranscriptEvent", {}).get("Transcript", {}).get("Results", [])
        for result in results:
            alternatives = result.get("Alternatives", [])
            if not alternatives:
                continue
            text = alternatives[0].get("Transcript", "")
            yield TranscriptChunk(text=text, is_partial=result.get("IsPartial", False), language_code=config.language_code)
