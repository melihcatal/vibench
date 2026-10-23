from typing import List, Dict, Any


def normalize_embedding_response(response: Any) -> List[Dict[str, Any]]:
    # Assuming response.data is a list of embedding objects
    # Each object has an 'embedding' attribute and potentially other info
    return [{'embedding': item.embedding} for item in response.data]


def prepare_batch_payload(texts: List[str], model: str = 'text-embedding-3-small') -> Dict[str, Any]:
    return {'input': texts, 'model': model}


def prepare_text_payload(text: str, model: str = 'text-embedding-3-small') -> Dict[str, Any]:
    return {'input': text, 'model': model}
