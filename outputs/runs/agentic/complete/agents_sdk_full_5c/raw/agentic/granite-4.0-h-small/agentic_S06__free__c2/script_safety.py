# [LATER-STEP] script_safety.py

from typing import Tuple
from google.cloud import dlp_v2 as dlp

def check_script_content(script: str) -> Tuple[bool, Optional[str]]:
    """Check a narration script for disallowed content using Google Cloud DLP.

    Args:
        script: Narration text to evaluate.

    Returns:
        Tuple (safe, info_message) where safe is True if no violations were found.
    """
    client = dlp.DlpServiceClient()
    # Define an info type set that captures profanity, hate speech, and personal data.
    info_types = [
        "US_PERSONAL_IDENTIFIER",
        "DETECTOR_PROFANITY",
        "DETECTOR_HATE_SPEECH"
    ]
    # Create an inspect request with content as string item.
    request = dlp.InspectContentRequest(
        parent=dlp.DlpServiceClient.organization_path("my-organization-id", "global"),
        inspect_config=dlp.InspectConfig(
            info_types=[dlp.InfoType(name=t) for t in info_types],
            min_likelihood=dlp.Likelihood.POSSIBLE,
        ),
        item=dlp.ContentItem(text_content=script),
    )
    response = client.inspect_content(request)
    findings = response.result.findings
    if findings:
        # Simple aggregation of unsafe info types.
        unsafe = set(ft.info_type.name for ft in findings)
        return False, f"Found unsafe content: {', '.join(unsafe)}"
    return True, None
