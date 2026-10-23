import os
from google.cloud import webrisk_v1
from security_models import DecryptionResponse

def check_payload_safety(payload: DecryptionResponse) -> bool:
    client = webrisk_v1.WebRiskServiceClient()
    parent = f"projects/{os.getenv('GCP_PROJECT_ID')}"
    threat_types = [
        webrisk_v1.ThreatType.MALWARE,
        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
        webrisk_v1.ThreatType.UNWANTED_SOFTWARE
    ]

    # Check if plaintext contains unsafe URLs
    plaintext_str = payload.plaintext.decode('utf-8', errors='ignore')
    response = client.search_uris(
        request={
            "parent": parent,
            "threat_types": threat_types,
            "uri": plaintext_str
        }
    )

    return not response.threat


def check_payload_for_secrets(payload: DecryptionResponse) -> bool:
    # Placeholder for secret detection logic
    plaintext_str = payload.plaintext.decode('utf-8', errors='ignore')
    secret_keywords = ["password", "api_key", "secret", "token"]
    return not any(keyword in plaintext_str.lower() for keyword in secret_keywords)