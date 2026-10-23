import os
from typing import List, Dict
from safety_client import get_openai_client
from safety_models import ModerationResult

def embed_moderation_rationales(results: List[ModerationResult]) -> Dict[str, List[float]]:
    client = get_openai_client()
    
    texts_to_embed = []
    text_ids = []

    for i, res in enumerate(results):
        rationale = f"Moderation decision for text: '{res.text}'. Overall status: {res.overall_decision}. Categories and violations: "
        violations = [f"{cat.category} (severity {cat.severity}, violates: {cat.violates})" for cat in res.categories]
        rationale += "; ".join(violations)
        
        texts_to_embed.append(rationale)
        text_ids.append(f"result_{i}")
    
    if not texts_to_embed:
        return {}

    model_id = "text-embedding-3-small"
    
    response = client.embeddings.create(input=texts_to_embed, model=model_id)

    embeddings_dict = {}
    for i, data in enumerate(response.data):
        embeddings_dict[text_ids[i]] = data.embedding
    
    return embeddings_dict
