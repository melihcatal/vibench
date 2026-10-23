from typing import List
from speech_client import get_aai_transcript
from speech_models import TranscriptSegment


def get_diarized_transcript(job_id: str) -> List[TranscriptSegment]:
    """Requests speaker diarization for a recorded meeting and returns the diarized segments using AssemblyAI."""
    result = get_aai_transcript(job_id)
    if result.segments is None:
        raise ValueError(
            "Diarization information not available. Ensure diarization was enabled during submission."
        )
    return result.segments
