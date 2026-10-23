import os
import json
from google.cloud import dlp_v2 as dlp

# Use Google Cloud DLP as the concrete provider for profiling moderation
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DEIDENTIFICATION_CONFIG = {
    "info_type": [],  # inspect all info types
    "min_likelihood": dlp.Likelihood.POSSIBLE,
    "limits": {
        "max_findings_per_request": 100,
    },
}

dlp_client = dlp.DlpServiceClient()


def profile_moderation(profile_text: str) -> str:
    """Moderate profile text before account activation.
    Flags/disallows disallowed content and returns a cleaned version.

    Provider identifier: Google Cloud DLP (https://cloud.google.com/dlp)
    """
    # Build item to inspect
    item = {
        "value": profile_text,
    }
    # Call DLP to find risky info
    response = dlp_client.inspect_content(
        request={
            "parent": f"projects/{PROJECT_ID}",
            "inspect_config": {
                "info_types": [*DEIDENTIFICATION_CONFIG["info_type"]],
                "min_likelihood": DEIDENTIFICATION_CONFIG["min_likelihood"],
            },
            "item": item,
        }
    )
    findings = response.result.findings
    if findings:
        # Simple policy: strip any finding and replace with redacted text
        clean_text = profile_text
        for finding in findings:
            clean_text = clean_text.replace(finding.info_type.name, "[REDACTED]")
        return clean_text
    return profile_text
