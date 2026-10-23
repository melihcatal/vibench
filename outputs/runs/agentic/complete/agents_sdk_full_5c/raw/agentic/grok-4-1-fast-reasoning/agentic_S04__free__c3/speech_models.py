from typing import List, Dict, Any, Optional

def get_transcript(job: Any) -> Optional[str]:
    return job.text if job and hasattr(job, 'status') and job.status == "completed" else None

def get_word_timestamps(job: Any) -> List[Dict[str, Any]]:
    if hasattr(job, 'words') and job.words:
        return [
            {
                "word": word.word,
                "start_ms": word.start,
                "end_ms": word.end,
                "confidence": getattr(word, 'confidence', None)
            }
            for word in job.words
        ]
    return []

def get_utterances(job: Any) -> List[Dict[str, Any]]:
    if hasattr(job, 'utterances') and job.utterances:
        return [
            {
                "speaker": ut.speaker,
                "text": ut.text,
                "start_ms": ut.start,
                "end_ms": ut.end
            }
            for ut in job.utterances
        ]
    return []