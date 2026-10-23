import os
from typing import List, Dict, Any
from google.cloud import dlp_v2

def check_secret_labels_for_safety(project_id: str, text_to_inspect: List[str]) -> Dict[str, Any]:
    """Checks secret labels and notes for unsafe text using Google Cloud DLP API.

    This function inspects a list of strings (e.g., secret labels, descriptions, notes)
    for sensitive information using Google Cloud DLP's inspect_content method.
    """
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"

    items = []
    for text in text_to_inspect:
        items.append({"value": text})

    # Configure the inspection request
    inspect_config = {
        "info_types": [{"name": "EMAIL_ADDRESS"}, {"name": "PHONE_NUMBER"}, {"name": "CREDIT_CARD_NUMBER"},
                       {"name": "IP_ADDRESS"}, {"name": "US_SOCIAL_SECURITY_NUMBER"}, {"name": "GENERIC_ID"}],
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0} # 0 means unlimited
    }

    try:
        response = client.inspect_content(
            request={
                "parent": parent,
                "inspect_config": inspect_config,
                "item": {"byte_item": {"type": dlp_v2.ByteContentItem.BytesType.TEXT_UTF8, "data": '\n'.join(text_to_inspect).encode('utf-8')}}
            }
        )

        findings_summary = []
        if response.result.findings:
            for finding in response.result.findings:
                findings_summary.append({
                    "info_type": finding.info_type.name,
                    "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                    "quote": finding.quote
                })
        
        return {
            "total_findings": len(response.result.findings),
            "findings": findings_summary
        }
    except Exception as e:
        raise ValueError(f"Error checking secret labels with Google Cloud DLP: {e}") from e
