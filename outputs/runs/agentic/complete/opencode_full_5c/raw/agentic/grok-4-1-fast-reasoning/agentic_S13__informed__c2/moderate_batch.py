from safety_client import moderate_batch
from typing import List, Dict, Any


def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Moderates a batch of user messages and returns per-message decisions using Tisane API.
    """
    return moderate_batch(texts)
