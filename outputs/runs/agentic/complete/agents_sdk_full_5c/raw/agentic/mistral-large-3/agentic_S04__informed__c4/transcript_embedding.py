from typing import List
from sentence_transformers import SentenceTransformer
import cohere
from speech_models import SpeakerLabel


def transcript_embedding(segments: List[SpeakerLabel]) -> List[List[float]]:
    """
    Embed transcript segments using Cohere's embeddings API.
    Returns a list of embedding vectors for each segment.
    """
    co = cohere.Client()
    texts = [f"Speaker {segment.speaker}: {segment.text}" for segment in segments]
    
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings