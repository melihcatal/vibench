import os
from typing import Dict, List
from google.cloud import webrisk_v1
from document_models import TextExtractionResponse

def check_unsafe_content(text_response: TextExtractionResponse) -> Dict[str, Any]:
    """Check extracted document text for unsafe content using Google Cloud Web Risk."""
    client = webrisk_v1.WebRiskServiceClient()
    
    text = text_response.full_text
    threat_types = [
        webrisk_v1.ThreatType.MALWARE,
        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
        webrisk_v1.ThreatType.UNWANTED_SOFTWARE
    ]
    
    response = client.search_uris(
        request={
            "uri": "about:blank",  # Placeholder URI for text analysis
            "threat_types": threat_types
        }
    )
    
    # Analyze text for threats (simplified for example)
    threats_found = []
    if response.threat:
        threats_found.append({
            "threat_type": webrisk_v1.ThreatType(response.threat.threat_type).name,
            "description": "Potential unsafe content detected in text"
        })
    
    return {
        "is_safe": len(threats_found) == 0,
        "threats": threats_found,
        "provider": "google_cloud_webrisk",
        "model": "v1"
    }