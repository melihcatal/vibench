from google.cloud import dlp_v2
from google.cloud.dlp_v2 import types

def check_payload_for_safety(project_id: str, text_payload: str) -> dict:
    """
    Checks a text payload for sensitive information using Google Cloud DLP.
    Returns a dictionary summarizing findings.
    """
    dlp_client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}/locations/global"

    # Define info types to detect
    info_types = [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}, {"name": "CREDIT_CARD_NUMBER"}, {"name": "US_SOCIAL_SECURITY_NUMBER"}]

    # Configure the inspect config
    inspect_config = types.InspectConfig(
        info_types=info_types,
        include_quote=True,
    )

    # Create the content item
    item = types.ContentItem(value=text_payload)

    # Request to inspect the content
    response = dlp_client.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    findings_summary = {
        "has_findings": False,
        "finding_count": 0,
        "findings": []
    }

    if response.result.findings:
        findings_summary["has_findings"] = True
        findings_summary["finding_count"] = len(response.result.findings)
        for finding in response.result.findings:
            findings_summary["findings"].append({
                "info_type": finding.info_type.name,
                "likelihood": types.Likelihood(finding.likelihood).name,
                "quote": finding.quote,
            })
    
    return findings_summary
