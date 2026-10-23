import os
from speech_client import get_comprehend_client
from speech_models import SafetyCheckRequest
from typing import List, Dict, Any

def check_script_safety(request: SafetyCheckRequest) -> List[Dict[str, Any]]:
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_pii_entities(
        Text=request.text,
        LanguageCode=request.language_code
    )
    return response['Entities']
