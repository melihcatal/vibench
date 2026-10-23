from observability_client import get_vertex_ai_embedding_model
from typing import List, Dict

def embed_log_messages(messages: List[str]) -> Dict[str, List[float]]:
    model = get_vertex_ai_embedding_model("text-embedding-004")

    embeddings_map: Dict[str, List[float]] = {}
    
    responses = model.embed_text(messages)
    
    for i, response in enumerate(responses):
        embeddings_map[messages[i]] = response.values
        
    return embeddings_map