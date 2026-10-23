from typing import List, Dict, Any
from speech_client import get_speech_client

def timestamped_transcript(job_id: str) -> List[Dict[str, Any]]:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != 'completed':
        raise ValueError(f'Transcript not completed: {transcript.status}')
    
    return [
        {
            'word': word.word,
            'start': round(word.start / 1000, 2),
            'end': round(word.end / 1000, 2),
            'confidence': word.confidence
        }
        for word in transcript.words
    ]