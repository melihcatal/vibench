import os
from google.cloud import webrisk_v1
from messaging_models import EventMessage

client = webrisk_v1.WebRiskServiceClient()

def check_message_safety(event: EventMessage) -> bool:
    text_content = " ".join(str(v) for v in event.payload.values())
    response = client.search_uris(
        request={
            "uri": f"http://example.com/?text={text_content}",
            "threat_types": [
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE
            ]
        }
    )
    return not response.threat