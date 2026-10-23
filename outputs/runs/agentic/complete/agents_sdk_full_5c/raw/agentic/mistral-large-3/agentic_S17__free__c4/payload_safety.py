import os
from google.cloud import webrisk_v1
from security_models import DecryptionResponse


def check_payload_safety(decrypted_payload: DecryptionResponse) -> dict:
    client = webrisk_v1.WebRiskServiceClient()
    
    request = {
        "uri": f"data:text/plain;base64,{_base64_encode(decrypted_payload.plaintext)}",
        "threat_types": [
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE
        ]
    }
    
    response = client.search_uris(request)
    
    return {
        "is_safe": not response.threat,
        "threats": [threat.type_.name for threat in response.threat.threat_types] if response.threat else [],
        "payload_key_id": decrypted_payload.key_id
    }


def _base64_encode(data: str) -> str:
    import base64
    return base64.b64encode(data.encode()).decode()