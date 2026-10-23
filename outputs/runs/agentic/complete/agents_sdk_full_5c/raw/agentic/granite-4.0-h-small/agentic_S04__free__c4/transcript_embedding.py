import os
import json
from typing import List, Dict
from speech_client import SpeechClient
from sentence_transformers import SentenceTransformer

# Provider-specific: Hugging Face Sentence Transformer model for embeddings
MODEL_ID = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_ID)

# Local utility: embed a list of transcript segments

def transcript_embedding(transcript_segments: List[Dict]) -> List[Dict]:
    """Compute sentence embeddings for each segment that contains text.

    Args:
        transcript_segments (List[Dict]): List of segment dicts produced by `timestamped_transcript`.
    Returns:
        List[Dict]: Original segment dicts enriched with an 'embedding' field (list of floats).
    """
    texts = [seg.get('word', '') for seg in transcript_segments if seg.get('word')]
    embeddings = model.encode(texts)
    for seg, emb in zip(transcript_segments, embeddings):
        seg['embedding'] = emb.tolist()
    return transcript_segments

if __name__ == '__main__':
    # Example usage - using placeholder transcript segments
    sample_segments = [
        {'start': 0.0, 'duration': 1.2, 'word': 'Hello world'},
        {'start': 1.5, 'duration': 0.9, 'word': 'Thank you for attending'}
    ]
    enriched = transcript_embedding(sample_segments)
    print('Embedded segments:', json.dumps(enriched, indent=2))
