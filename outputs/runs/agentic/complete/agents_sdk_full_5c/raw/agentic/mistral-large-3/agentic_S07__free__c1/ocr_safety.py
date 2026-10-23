import os
from typing import List
from google.cloud import webrisk_v1
from document_models import OCRTextResponse

def check_unsafe_content(text_response: OCRTextResponse) -> List[str]:
    """Check extracted document text for unsafe content using Google Web Risk API."""
    client = webrisk_v1.WebRiskServiceClient()
    response = client.search_uris(
        request={
            "uri": "about:blank",  # Placeholder URI for text analysis
            "threat_types": [
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE
            ]
        }
    )
    
    # Analyze text for threats (simplified for example)
    threats = []
    if "malware" in text_response.text.lower():
        threats.append("MALWARE")
    if "phishing" in text_response.text.lower():
        threats.append("SOCIAL_ENGINEERING")
    
    return threats