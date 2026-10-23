import os
import cohere
from typing import List
from safety_models import EmbeddingResult

def embed_moderation_reasons(reasons: List[str]) -> List[EmbeddingResult]:
    """
    Embeds moderation rationale strings for case retrieval using Cohere.

    :param reasons: A list of text strings (moderation rationales).
    :return: A list of EmbeddingResult objects.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(api_key)
    
    model_name = "embed-english-v3.0"

    try:
        response = co.embed(
            texts=reasons,
            model=model_name,
            input_type="search_document"
        )
        
        results = []
        for i, embedding in enumerate(response.embeddings):
            results.append(EmbeddingResult(text=reasons[i], embedding=embedding))
        return results

    except cohere.CohereError as e:
        # Handle API errors gracefully
        print(f"Cohere API error: {e}")
        return [EmbeddingResult(text=reason, embedding=[]) for reason in reasons]
