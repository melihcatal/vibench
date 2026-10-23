from typing import Literal, NamedTuple

class SynthesisRequest(NamedTuple):
    text: str
    voice_id: str = "Joanna"  # AWS Polly default voice
    output_format: Literal["mp3", "ogg_vorbis", "pcm"] = "mp3"

class SynthesisResponse(NamedTuple):
    audio_stream: bytes
