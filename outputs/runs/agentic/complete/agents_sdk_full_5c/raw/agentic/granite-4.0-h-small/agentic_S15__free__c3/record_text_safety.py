# record_text_safety.py
# [LATER-STEP] Detect unsafe content in document fields using Azure Content Safety API

import os
import requests
from typing import Dict, Any

CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_API_KEY = os.getenv("CONTENT_SAFETY_API_KEY")

if not CONTENT_SAFETY_ENDPOINT or not CONTENT_SAFETY_API_KEY:
    raise RuntimeError("Content Safety credentials not configured")

def check_unsafe_content(document: Dict[str, Any], unsafe_fields: list = None) -> bool:
    """Return True if any selected text field contains unsafe material."""
    
    if unsafe_fields is None:
        # sensible defaults: any string field potentially user‑generated
        unsafe_fields = [k for k, v in document.items() if isinstance(v, str)]
    
    payload = {
        "contentProperties": [{"id": f"field_{i}", "type": "text", "text": document[k]}
                               for i, k in enumerate(unsafe_fields)]
    }
    
    response = requests.post(
        f"{CONTENT_SAFETY_ENDPOINT}/contentSafety/moderate",
        json=payload,
        headers={"Ocp-Apim-Subscription-Key": CONTENT_SAFETY_API_KEY}
    )
    response.raise_for_status()
    result = response.json()
    
    # The API returns a list of detected issues under `identifiedIssues`
    unsafe = any(issue.get("category") == "unwanted" for issue in result.get("identifiedIssues", []))
    return unsafe
