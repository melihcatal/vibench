from typing import List, Dict, Any
from safety_client import ComprehendSafetyClient
from safety_models import BatchModerationRequest, BatchModerationResponse, TextModerationResponse

def moderate_batch(texts: List[str], config: Dict[str, Any] = None) -> BatchModerationResponse:
    config = config or {}
    client = ComprehendSafetyClient(region_name=config.get("region", "us-east-1"))
    
    request = BatchModerationRequest(texts=texts, language_code=config.get("language_code", "en"))
    results: List[TextModerationResponse] = client.batch_detect_toxic_content(request)

    return BatchModerationResponse(results=results)
