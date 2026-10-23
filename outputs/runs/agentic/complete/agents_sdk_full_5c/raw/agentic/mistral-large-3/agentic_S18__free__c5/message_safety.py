import os
from google.cloud import webrisk_v1
from typing import Dict

client = webrisk_v1.WebRiskServiceClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")

def check_message_safety(text: str) -> bool:
    request = webrisk_v1.SearchUrisRequest(
        uri=text,
        threat_types=[
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
        ],
    )
    
    response = client.search_uris(request=request)
    return not response.threat


def check_payload_safety(payload: Dict) -> bool:
    text = str(payload)
    return check_message_safety(text)