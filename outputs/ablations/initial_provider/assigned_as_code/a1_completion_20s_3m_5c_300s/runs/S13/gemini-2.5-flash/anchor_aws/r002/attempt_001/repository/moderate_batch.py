import boto3
from typing import List, Dict, Any
from safety_client import get_aws_client
from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationResult

def moderate_batch(payload: BatchModerationRequest, config: Dict[str, Any] = None) -> BatchModerationResponse:
    config = config or {}
    client = get_aws_client("comprehend", region_name=config.get("region", "us-east-1"))
    
    text_segments = [{
        "Text": text
    } for text in payload.texts]

    response = client.batch_detect_toxic_content(TextSegments=text_segments, LanguageCode="en")
    
    results = []
    for i, result in enumerate(response["ResultList"]):
        results.append(ModerationResult(
            text=payload.texts[i],
            categories=result["Toxicity"]
        ))
    
    return BatchModerationResponse(results=results)
