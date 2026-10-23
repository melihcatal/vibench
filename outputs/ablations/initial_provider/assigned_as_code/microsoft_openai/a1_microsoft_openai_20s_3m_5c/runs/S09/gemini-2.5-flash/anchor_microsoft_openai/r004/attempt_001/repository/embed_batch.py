from typing import List, Dict, Any
from embeddings_client import EmbeddingsClient
from embeddings_models import BatchEmbeddingResponse

def embed_batch(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, List[List[float]]]:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get('api_key'))
    
    texts = payload['texts']
    model = payload.get('model', 'text-embedding-3-small') # Default to the same model as embed_text.py
    
    response: BatchEmbeddingResponse = client.embed(texts=texts, model=model)
    return {'embeddings': response.embeddings}
