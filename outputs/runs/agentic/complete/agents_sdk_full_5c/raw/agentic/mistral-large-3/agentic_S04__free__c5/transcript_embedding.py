from sentence_transformers import SentenceTransformer
from typing import List
from speech_models import TranscriptSegment

def embed_transcript_segments(segments: List[TranscriptSegment]) -> List[List[float]]:
    """Embed transcript segments for semantic retrieval using Cohere's multilingual model via Sentence Transformers."""
    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")  # Cohere-backed model
    
    segment_texts = [segment.text for segment in segments]
    embeddings = model.encode(segment_texts, convert_to_tensor=False)
    
    return embeddings.tolist()