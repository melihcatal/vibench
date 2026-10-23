from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextEmbeddingModel
from speech_models import SpeechRecognitionResult
from typing import Iterator, List, Dict, Any

class CaptionEmbedder:
    def __init__(self, project_id: str, location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        # Using the latest text embedding model, check Vertex AI documentation for current versions
        self._model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    def embed_captions(self, captions_text: List[str]) -> List[List[float]]:
        if not captions_text:
            return []

        # Vertex AI Generative AI for embeddings
        # The model returns a list of embeddings, one for each input text.
        embeddings = self._model.get_embeddings(captions_text)
        return [embedding.values for embedding in embeddings]

def caption_embedding(caption_chunks: Iterator[SpeechRecognitionResult], project_id: str) -> Iterator[Dict[str, Any]]:
    embedder = CaptionEmbedder(project_id)
    
    # Collect captions to embed in batches or when a final caption is received
    batch_for_embedding = []
    for chunk in caption_chunks:
        batch_for_embedding.append(chunk.text)
        if chunk.is_final and batch_for_embedding: # Embed when a final chunk is received and there's text to embed
            embeddings = embedder.embed_captions(batch_for_embedding)
            yield {"caption_texts": batch_for_embedding, "embeddings": embeddings, "is_final_segment": True}
            batch_for_embedding = [] # Reset for the next segment
        elif not chunk.is_final:
            # For non-final chunks, we might accumulate them or embed them as they come if real-time embedding is critical.
            # For simplicity, here we're accumulating until a final chunk or end of stream.
            pass # Accumulate for now, will be embedded when a final chunk comes.
    
    # Embed any remaining captions if the stream ends without a final chunk
    if batch_for_embedding:
        embeddings = embedder.embed_captions(batch_for_embedding)
        yield {"caption_texts": batch_for_embedding, "embeddings": embeddings, "is_final_segment": True}
