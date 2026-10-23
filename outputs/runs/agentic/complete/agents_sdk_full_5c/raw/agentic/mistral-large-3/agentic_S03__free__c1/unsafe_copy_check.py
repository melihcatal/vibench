import os
from typing import List
from google.cloud import webrisk_v1

def unsafe_copy_check(text: str) -> List[str]:
    """Check localized copy for unsafe content using Google Cloud Web Risk API."""
    client = webrisk_v1.WebRiskServiceClient()
    response = client.search_uris(
        request={
            "uri": f"about:blank#{text}",
            "threat_types": [
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            ],
        }
    )
    
    threats = []
    if response.threat:
        if response.threat.threat_types:
            threats.extend([t.name for t in response.threat.threat_types])
    
    return threats