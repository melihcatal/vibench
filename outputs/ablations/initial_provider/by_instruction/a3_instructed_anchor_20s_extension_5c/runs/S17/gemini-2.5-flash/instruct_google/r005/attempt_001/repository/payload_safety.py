from google.cloud import dlp_v2
from security_models import PayloadSafetyRequest, PayloadSafetyResponse
from google.cloud.dlp_v2.types import InspectConfig, ContentItem

def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    """
    Checks decrypted text payloads for unsafe content using Google Cloud DLP (Data Loss Prevention).
    """
    dlp_client = dlp_v2.DlpServiceClient()

    # The parent project ID for the DLP request. This typically comes from an environment variable or config.
    # For simplicity, we assume a default project or it's implicitly handled by credentials.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        # Fallback if env var not set, for demonstration.
        # In a real app, this should be configured properly.
        print("GOOGLE_CLOUD_PROJECT_ID environment variable not set. Using 'your-gcp-project-id'.")
        project_id = "your-gcp-project-id"

    parent = f"projects/{project_id}/locations/global"

    # Configure the inspection
    inspect_config = InspectConfig(
        info_types=[
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
            {"name": "US_SOCIAL_SECURITY_NUMBER"},
            {"name": "IP_ADDRESS"},
            {"name": "GENERIC_PII"},
            # Add more info types as needed
        ],
        min_likelihood=request.min_likelihood,
        include_quote=True, # Include the sensitive content found
    )

    # The content to inspect
    item = ContentItem(value=request.content)

    # Perform the inspection
    response = dlp_client.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    has_unsafe_content = bool(response.result.findings)
    findings = []
    if has_unsafe_content:
        for finding in response.result.findings:
            findings.append({
                "info_type": finding.info_type.name,
                "likelihood": finding.likelihood.name,
                "quote": finding.quote,
                "start_index": finding.location.byte_range.start,
                "end_index": finding.location.byte_range.end,
            })

    return PayloadSafetyResponse(has_unsafe_content=has_unsafe_content, findings=findings)

import os # Ensure os is imported for os.environ.get
