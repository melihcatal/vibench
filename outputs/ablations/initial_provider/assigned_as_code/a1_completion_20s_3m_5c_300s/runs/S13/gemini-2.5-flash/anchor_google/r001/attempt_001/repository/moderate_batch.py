from typing import List, Dict, Any
from safety_client import SafetyClient
from safety_models import BatchModerationRequest, BatchModerationResult, ModerationResult
import os

def moderate_batch(texts: List[str], config: Dict[str, Any] = None) -> List[BatchModerationResult]:
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("API key not provided or found in environment variables.")

    client = SafetyClient(api_key=api_key)
    request = BatchModerationRequest(texts=texts)
    batch_results = client.moderate_batch(request)
    return batch_results
