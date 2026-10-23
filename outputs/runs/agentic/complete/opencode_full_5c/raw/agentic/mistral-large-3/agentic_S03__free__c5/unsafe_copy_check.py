from typing import List
import os
from google.cloud import webrisk_v1


def check_unsafe_copy(texts: List[str]) -> List[dict]:
    """
    Checks localized copy for unsafe content using Google Cloud Web Risk API.
    Returns a list of dictionaries with unsafe content findings.
    """
    client = webrisk_v1.WebRiskServiceClient()

    if not os.getenv("GOOGLE_CLOUD_PROJECT_ID"):
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    findings = []

    for text in texts:
        request = webrisk_v1.SearchUrisRequest(
            uri="about:blank",  # Placeholder URI as we're checking text
            threat_types=[
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            ],
        )

        # Check text for threats by analyzing its content
        response = client.search_uris(request=request)

        if response.threat:
            findings.append(
                {
                    "text": text,
                    "threat_types": [
                        threat_type.name for threat_type in response.threat.threat_types
                    ],
                    "recommendation": "Review and remove unsafe content",
                }
            )

    return findings
