# [LATER-STEP] moderation_reason_embedding.py

from safety_client import get_content_safety_client
from safety_models import SafetyRequest, SafetyResponse
import numpy as np
from ibm_watsonx_ai.embedding import EmbeddingModel, EmbeddingInput

# Embed moderation rationales (e.g., unsafe spans) for case retrieval
# Uses IBM watsonx.ai embeddings (scorable provider)

def embed_moderation_reasons(text: str, spans: List[Span]) -> np.ndarray:
    """Embeds the provided text and the extracted unsafe spans for similarity search.

    Returns concatenated embeddings: [text_embedding, span_embedding].
    """
    client = get_content_safety_client()  # uses AWS Bedrock Guardrails as default provider
    # 1. Embed the whole text
    text_embedding = client.embed(text=text)
    # Ensure we get a numpy array of shape (model_dim,)
    text_emb = np.array(text_embedding.embedding) if hasattr(text_embedding, "embedding") else np.zeros(512)

    # 2. Embed each unsafe span (as substring) and average them
    span_embeddings = []
    for span in spans:
        span_text = text[span.start:span.end]
        span_embedding = client.embed(text=span_text)
        span_embeddings.append(np.array(span_embedding.embedding) if hasattr(span_embedding, "embedding") else np.zeros(512))
    if span_embeddings:
        span_emb = np.mean(span_embeddings, axis=0)
    else:
        span_emb = np.zeros(512)

    # 3. Concatenate embeddings as a single vector for downstream retrieval
    return np.concatenate([text_emb, span_emb])
