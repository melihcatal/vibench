from dataclasses import dataclass


@dataclass
class StreamingAudioRequest:
    sample_rate_hz: int
    language_code: str
    audio_chunks: list


def normalize_transcript(text, is_final=False, language_code=None):
    return {"text": text.strip(), "is_final": bool(is_final), "language_code": language_code}


def normalize_chunk(chunk):
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    return bytes(chunk)
