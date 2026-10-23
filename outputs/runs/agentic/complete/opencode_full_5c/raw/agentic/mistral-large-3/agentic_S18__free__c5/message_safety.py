from typing import Dict, Optional
import os


def message_safety(payload: Dict) -> Dict:
    """
    Checks message payload text for unsafe content using Google Cloud's
    Web Risk API to detect malicious or inappropriate content.

    Args:
        payload: Dictionary containing message data.

    Returns:
        Dict: Safety check results, including threats and recommendations.
    """
    from google.cloud import webrisk_v1

    client = webrisk_v1.WebRiskServiceClient()
    text = payload.get("content", "")

    result = {"is_safe": True, "threats": [], "recommendation": "No action required"}

    if not text:
        return result

    # Check for unsafe content
    response = client.search_uris(
        request={
            "uri": f"text:{text}",
            "threat_types": [
                webrisk_v1.ThreatType.MALWARE,
                webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            ],
        }
    )

    if response.threat:
        result["is_safe"] = False
        result["threats"] = [
            threat.type_.name for threat in response.threat.threat_types
        ]
        result["recommendation"] = "Review or discard this message"

    return result
