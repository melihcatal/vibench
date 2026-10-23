import json
from typing import Any

def archive_summary(transcript: str, job_id: str) -> str:
    """Generate a concise summary of the transcription for archival.
    
    The summary extracts speaker count (via placeholders) and word count.
    In a real system this could call a summarization model.
    """
    word_count = len(transcript.split())
    # Placeholder: if a hosted summarization API existed, we would call it here.
    summary = {
        'job_id': job_id,
        'word_count': word_count,
        # 'segments': hosted_summarizer.summarize(transcript)   # not a real call
    }
    return json.dumps(summary, indent=2)
