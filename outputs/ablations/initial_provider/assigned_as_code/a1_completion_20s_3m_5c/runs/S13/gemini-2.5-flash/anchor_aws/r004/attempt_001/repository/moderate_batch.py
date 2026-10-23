import boto3
from typing import List, Dict, Any
from safety_client import get_aws_client
from safety_models import BatchTextModerationRequest, TextModerationResult

def moderate_batch(payload: BatchTextModerationRequest, config: Dict[str, Any] = None) -> List[TextModerationResult]:
    config = config or {}
    client = get_aws_client("comprehend", config)
    
    text_segments = [{
        "Text": text
    } for text in payload.texts]

    response = client.detect_toxic_content(
        TextSegments=text_segments,
        LanguageCode=payload.language_code
    )

    results = []
    for i, result in enumerate(response["ResultList"]):
        results.append(TextModerationResult(
            text=payload.texts[i],
            is_safe=result["Toxicity"]["Value"] < config.get("toxicity_threshold", 0.5), # Placeholder for safety decision
            scores=result["Toxicity"],
            categories=result["Categories"]
        ))
    return results
