from typing import List, Dict, Any
from embeddings_client import get_openai_client
from embeddings_models import prepare_batch_payload, normalize_embedding_response


def embed_batch(texts: List[str], config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    
    # Use the same model as embed_text.py
    model_name = 'text-embedding-3-small' 
    
    payload = prepare_batch_payload(texts, model=model_name)
    response = client.embeddings.create(**payload)
    return normalize_embedding_response(response)
