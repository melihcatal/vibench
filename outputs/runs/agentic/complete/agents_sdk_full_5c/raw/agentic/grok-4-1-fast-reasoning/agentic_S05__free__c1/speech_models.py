from typing import bytesvalue
def prepare_audio_chunk(chunk: bytes) -> bytes:
    # Placeholder normalization for Deepgram Live: expects raw PCM 16kHz mono S16LE
    return chunk

class StreamingTranscript:
    transcript: str
    is_final: bool

    def __init__(self, transcript: str, is_final: bool = False):
        self.transcript = transcript
        self.is_final = is_final