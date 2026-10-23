import os
from typing import List
import cohere
from speech_models import TranscriptSegment

def embed_transcript_segments(segments: List[TranscriptSegment]) -> List[List[float]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere.

    Args:
        segments: A list of TranscriptSegment objects.

    Returns:
        A list of embedding vectors, one for each segment.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)
    
    texts_to_embed = [segment.text for segment in segments]
    
    if not texts_to_embed:
        return []

    response = co.embed(
        texts=texts_to_embed,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings
