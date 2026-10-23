from typing import List, Dict, Any
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client
from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationResponse

def moderate_batch(batch_request: BatchModerationRequest, config: Dict[str, Any] = None) -> BatchModerationResponse:
    config = config or {}
    client = get_content_safety_client(config['endpoint'], config['api_key'])
    results = []
    for text in batch_request.texts:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
        categories = {category.category: category.severity for category in response.categories_analysis}
        decision = "unsafe" if any(s > 0 for s in categories.values()) else "safe" # Simplified decision logic
        results.append(ModerationResponse(text=text, categories=categories, decision=decision, raw_response=response))
    return BatchModerationResponse(results=results)
