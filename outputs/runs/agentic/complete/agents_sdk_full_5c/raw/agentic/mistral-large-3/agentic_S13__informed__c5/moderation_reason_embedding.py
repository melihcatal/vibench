# Embed moderation rationales for case retrieval using Cohere Embed API

import os
from typing import List
import cohere
from safety_models import SafetyDecision


def embed_moderation_reason(decisions: List[SafetyDecision]) -> List[float]:
    """Embed moderation rationales for case retrieval using Cohere Embed API."""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    reason_texts = []
    for decision in decisions:
        if decision["flagged"]:
            reason_texts.append(
                f"Flagged for {decision['category']} with score {decision['score']:.2f}."
            )
    
    if not reason_texts:
        reason_texts.append("No moderation issues detected.")
    
    response = co.embed(texts=reason_texts, model="embed-english-v3.0")
    return response.embeddings[0]