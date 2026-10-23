from typing import Dict, Optional

from speech_models import TranscriptChunk, transcript_chunk_from_deepgram


def handle_partial_result(event: Dict[str, object]) -> Optional[TranscriptChunk]:
    chunk = transcript_chunk_from_deepgram(event)
    if not chunk.text:
        return None
    return chunk
