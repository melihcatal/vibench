from typing import List
import os
from google.cloud import webrisk_v1


def check_unsafe_copy(texts: List[str]) -> Dict[str, List[str]]:
    """Check localized copy for unsafe content using Google Cloud Web Risk API."""
    client = webrisk_v1.WebRiskServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    threats = {"MALWARE": [], "SOCIAL_ENGINEERING": [], "UNWANTED_SOFTWARE": []}

    for text in texts:
        response = client.search_uris(
            request={
                "uri": f"http://example.com/?q={text}",
                "threat_types": [
                    webrisk_v1.ThreatType.MALWARE,
                    webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                    webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
                ],
            }
        )

        for threat in response.threat.threat_types:
            threats[threat.name].append(text)

    return threats
