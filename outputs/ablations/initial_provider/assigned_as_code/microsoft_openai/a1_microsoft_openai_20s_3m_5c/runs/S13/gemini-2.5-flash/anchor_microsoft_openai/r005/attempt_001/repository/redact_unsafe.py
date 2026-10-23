from typing import Dict, Any
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client
from safety_models import RedactionResponse

def redact_unsafe_text(text: str, config: Dict[str, Any] = None, threshold: float = 0.5) -> RedactionResponse:
    config = config or {}
    client = get_content_safety_client(config['endpoint'], config['api_key'])
    response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
    
    categories = {category.category: category.severity for category in response.categories_analysis}
    
    is_unsafe = False
    for severity in categories.values():
        if severity / 7 > threshold:  # Normalize severity to 0-1 range and compare with threshold
            is_unsafe = True
            break

    redacted_text = "[REDACTED_UNSAFE_CONTENT]" if is_unsafe else text
    
    # Since Azure Content Safety doesn't provide specific spans for generic unsafe content categories,
    # we'll represent redaction as a single span covering the whole text if it's unsafe.
    spans = []
    if is_unsafe:
        spans.append({"offset": 0, "length": len(text), "replacement": "[REDACTED_UNSAFE_CONTENT]"})
        
    return RedactionResponse(original_text=text, redacted_text=redacted_text, categories=categories, spans=spans)
