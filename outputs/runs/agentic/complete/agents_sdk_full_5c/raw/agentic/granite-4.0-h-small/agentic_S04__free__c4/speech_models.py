from typing import Dict, List, Union

TranscriptionResult = Dict[str, Any]
JobStatus = Dict[str, Any]
TimestampSegment = Dict[str, Union[str, float]]

SpeechJobRequest = Dict[str, Any]
TranscriptRequest = Dict[str, Union[str, int]]

def normalize_job_response(raw: JobStatus) -> JobStatus:
    """Convert platform-specific fields to a common schema."""
    return {
        'job_id': raw.get('id'),
        'status': raw.get('status'),
        'created_at': raw.get('created_at'),
        'updated_at': raw.get('updated_at'),
        'output_url': raw.get('outputUrl')
    }


def normalize_timestamps(raw: List[Any]) -> List[TimestampSegment]:
    """Convert raw timing payload to a list of segment dicts."""
    normalized = []
    for seg in raw:
        normalized.append({
            'start': seg.get('start'),
            'duration': seg.get('duration'),
            'speaker': seg.get('speaker'),
            'word': seg.get('word')
        })
    return normalized