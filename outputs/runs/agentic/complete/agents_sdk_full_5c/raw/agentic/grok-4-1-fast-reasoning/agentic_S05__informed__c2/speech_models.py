import numpy as np
from typing import NamedTuple

class AudioConfig(NamedTuple):
    sample_rate_hertz: int = 16000
    channels: int = 1
    encoding: str = 'LINEAR16'

def pcm16_to_bytes(audio_data: np.ndarray) -> bytes:
    """Convert float32 or int16 numpy array to LINEAR16 bytes."""
    if audio_data.dtype == np.float32:
        audio_int16 = (audio_data * 32767).astype(np.int16)
    else:
        audio_int16 = audio_data.astype(np.int16)
    return audio_int16.tobytes()