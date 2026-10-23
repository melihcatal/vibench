from google.cloud import dlp_v2

def check_unsafe_content(text: str) -> dict:
    """
    Checks localized copy for unsafe content using Google Cloud Data Loss Prevention (DLP) API.
    This example checks for common sensitive info types, which can be extended for "unsafe" content.
    """
    client = dlp_v2.DlpServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}/locations/global"

    item = {"value": text}

    # Define info types to inspect. This can be customized for specific "unsafe" categories.
    # For a general "unsafe" check, one might include categories related to hate speech,
    # violence, etc., which are often handled by content moderation APIs.
    # DLP is more geared towards PII/sensitive data. For true "unsafe" content,
    # other services like Perspective API (Jigsaw) or custom ML models might be more suitable.
    # For this exercise, we'll use DLP with some general categories.
    info_types = [
        {"name": "PHONE_NUMBER"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "PERSON_NAME"},
        {"name": "DATE_OF_BIRTH"},
    ]

    response = client.inspect_content(
        request={
            "parent": parent,
            "inspect_config": {"info_types": info_types, "min_likelihood": dlp_v2.Likelihood.POSSIBLE},
            "item": item,
        }
    )

    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append({
                "info_type": finding.info_type.name,
                "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                "quote": finding.quote,
            })

    return {
        "has_unsafe_content": bool(findings),
        "findings": findings,
        "note": "This check focuses on sensitive data. For broader 'unsafe' content (e.g., hate speech), consider additional content moderation APIs like Perspective API."
    }
