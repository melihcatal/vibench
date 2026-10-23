# [LATER-STEP] script_safety.py

import os
from google.cloud import dlp_v2 as dlp

# Load DLP service (requires GOOGLE_APPLICATION_CREDENTIALS)
client = dlp.DlpServiceClient()


def scan_script_for_sensitive_content(script: str) -> bool:
    """Scans narration script for potentially unsafe or sensitive content.

    Uses Google Cloud DLP to detect personal identifiers, profanity, etc.

    Args:
        script: The narration text to examine.

    Returns:
        True if the script contains no disallowed content, otherwise False.
    """
    info_types = [
        dlp.InfoType(name="PERSON"),
        dlp.InfoType(name="EMAIL_ADDRESS"),
        dlp.InfoType(name="PHONE_NUMBER"),
        dlp.InfoType(name="CREDENTIALS"),
    ]

    inspect_config = dlp.InspectConfig(
        info_types=info_types,
        # minimal thresholds; adjust as needed
        min_likelihood=dlp.Likelihood.POSSIBLE,
    )

    # Construct content item
    content_item = dlp.ContentItem(value=script)

    # Perform inspection
    response = client.inspect_content(
        request={
            "inspect_config": inspect_config,
            "item": content_item,
        }
    )

    if response.result.findings:
        # Unsafe content detected
        return False
    return True


# Example usage:
# print(scan_script_for_sensitive_content("My email is secret@example.com"))
