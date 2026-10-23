from dataclasses import dataclass


@dataclass
class AudioChunkStreamRequest:
    audio_chunks: list
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    show_speaker_label: bool = False
    enable_partial_results_stabilization: bool = True
    enable_channel_identification: bool = False
    vocabulary_name: str | None = None
    model_name: str | None = None


def normalize_caption_event(text, is_final=False, language_code="en-US", **extra):
    payload = {"text": text, "is_final": bool(is_final), "language_code": language_code}
    payload.update(extra)
    return payload


def normalize_chunk(chunk):
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    return bytes(chunk)
