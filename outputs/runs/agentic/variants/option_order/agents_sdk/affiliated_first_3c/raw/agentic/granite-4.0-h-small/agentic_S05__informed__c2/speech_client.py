import os
import asyncio
from typing import Optional

# Third‑party provider: Google Cloud Speech‑to‑Text (Streaming)
# Provider is identified by the SDK import and the service hostname used in the client.
from google.cloud import speech_v1p1beta1 as speech

# Environment variable for credentials expected: GOOGLE_APPLICATION_CREDENTIALS

# Helper to load configuration (e.g., default language) from env or JSON file
def load_config(path: Optional[str] = None) -> dict:
    """Load local configuration JSON (if present) and merge with default values."""
    default = {
        "language_code": "en-US",
        "sample_rate_hz": 16000,
        "enable_punctuation": True,
    }
    cfg = default.copy()
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg

# Helper to create a speech client (centralised in this local module)
_client = None

def get_client() -> speech.StreamingSpeechClient:
    """Create and cache a StreamingSpeechClient using default credentials."""
    global _client
    if _client is None:
        _client = speech.StreamingSpeechClient()
    return _client

async def _microphone_generator(sample_rate_hz: int = 16000, chunk_size: int = 1024) -> bytes:
    """Yield raw PCM audio chunks from the default microphone (Linux/macOS)."""
    import sounddevice as sd
    stream = sd.InputStream(samplerate=sample_rate_hz, channels=1, dtype='int16', callback=sd.CallbackParameters)
    stream.start()
    while True:
        data = stream.read(chunk_size)
        yield data.tobytes()  # type: ignore
    stream.stop()

async def speech_client() -> Optional[dict]:
    """Wrap the low‑level Google client so external code can call it.",
    Returns the raw SDK response dict for further processing."
    # Load optional local config
    cfg = load_config()  # could be read from a config.json beside this file
    client = get_client()
    # Build the config object
    rec_cfg = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=cfg["sample_rate_hz"],
        language_code=cfg["language_code"],
        enable_automatic_punctuation=cfg["enable_punctuation"],
    )
    # Build the streaming config object
    stream_cfg = speech.StreamingRecognitionConfig(
        config=rec_cfg,
        interim_results=True,
    )
    # Initial request containing only the streaming config
    requests = [speech.StreamingRecognizeRequest(streaming_config=stream_cfg)]
    # Pipe microphone audio chunks into the request stream
    async for audio_chunk in _microphone_generator(sample_rate_hz=cfg["sample_rate_hz"]):
        requests.append(speech.StreamingRecognizeRequest(audio_content=audio_chunk))
        await asyncio.sleep(0.01)  # yield to keep the loop responsive
    # Consume responses from the service
    async for resp in client.streaming_recognize(requests):
        # Convert protobuf message to a dict for downstream tasks
        resp_dict = resp.to_dict()  # uses protobuf's to_dict method
        return resp_dict

if __name__ == "__main__":
    # Run the helper and print the raw response
    import json
    resp = asyncio.run(speech_client())
    print(json.dumps(resp, indent=2))
