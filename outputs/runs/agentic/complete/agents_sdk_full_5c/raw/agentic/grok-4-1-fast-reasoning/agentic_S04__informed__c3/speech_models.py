import assemblyai as aai
from typing import List, Dict, Any

def get_transcript_text(transcript: aai.Transcript) -> str:
    if transcript.status != aai.TranscriptStatus.completed:
        raise ValueError(f'Transcript not completed: {transcript.status}')
    return transcript.text

def get_diarized_words(transcript: aai.Transcript) -> List[Dict[str, Any]]:
    words = []
    for word in transcript.words or []:
        words.append({
            'text': word.text,
            'start_ms': word.start,
            'end_ms': word.end,
            'speaker': getattr(word, 'speaker', None),
            'confidence': getattr(word, 'confidence', None)
        })
    return words