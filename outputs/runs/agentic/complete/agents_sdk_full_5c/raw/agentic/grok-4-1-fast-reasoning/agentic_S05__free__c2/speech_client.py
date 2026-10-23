import pyaudio
from typing import Dict, Any, Tuple

AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHUNK_SIZE = 1600

def get_audio_config() -> Dict[str, Any]:
    return {
        "format": AUDIO_FORMAT,
        "channels": AUDIO_CHANNELS,
        "rate": AUDIO_RATE,
        "frames_per_buffer": AUDIO_CHUNK_SIZE,
    }

def setup_microphone() -> Tuple[pyaudio.PyAudio, pyaudio.Stream]:
    p = pyaudio.PyAudio()
    config = get_audio_config()
    stream = p.open(input=True, **config)
    return p, stream

def close_microphone(p: pyaudio.PyAudio, stream: pyaudio.Stream):
    stream.stop_stream()
    stream.close()
    p.terminate()