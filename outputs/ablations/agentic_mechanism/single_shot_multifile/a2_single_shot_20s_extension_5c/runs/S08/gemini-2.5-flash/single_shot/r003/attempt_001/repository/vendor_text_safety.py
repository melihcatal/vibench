import os
from document_client import get_openai_client
from document_models import ModerationRequest
from typing import Dict, Any

def moderate_vendor_notes(request: ModerationRequest) -> Dict[str, Any]:
    if not request.text:
        return {"flagged": False, "categories": {}, "category_scores": {}}

    client = get_openai_client()

    try:
        response = client.moderations.create(input=request.text)
        result = response.results[0]
        
        return result.model_dump()
    except Exception as e:
        return {"error": str(e), "flagged": True, "categories": {"api_error": True}, "category_scores": {}}