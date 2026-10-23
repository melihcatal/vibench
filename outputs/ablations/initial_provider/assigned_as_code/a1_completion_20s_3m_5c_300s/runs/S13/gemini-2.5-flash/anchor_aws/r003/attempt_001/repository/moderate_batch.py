import boto3
from typing import List, Dict, Any
from safety_client import get_comprehend_client
from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationResponse

def moderate_batch(batch_request: BatchModerationRequest, config: Dict[str, Any] = None) -> BatchModerationResponse:
    config = config or {}
    client = get_comprehend_client(config.get("region", "us-east-1"))
    
    results = []
    for item in batch_request.texts:
        text = item["text"]
        message_id = item.get("message_id")
        
        response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
        toxicity_score = response["ResultList"][0]["Toxicity"]
        
        # For simplicity, let's consider text unsafe if toxicity score is above a threshold (e.g., 0.5)
        is_safe = toxicity_score < config.get("toxicity_threshold", 0.5)
        
        results.append(ModerationResponse(
            message_id=message_id,
            is_safe=is_safe,
            moderation_results={"toxicity": toxicity_score}
        ))
        
    return BatchModerationResponse(results=results)
