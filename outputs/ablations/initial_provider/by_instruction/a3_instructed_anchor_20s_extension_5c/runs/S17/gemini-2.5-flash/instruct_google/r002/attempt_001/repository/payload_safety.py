import os
from google.cloud import dlp_v2
from security_models import PlaintextPayload

def check_payload_safety(payload: PlaintextPayload, project_id: str) -> dict:
    dlp_client = dlp_v2.DlpServiceClient()
    project_path = f"projects/{project_id}"

    # Configure the inspect request to look for common sensitive info types
    inspect_config = {
        "info_types": [
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
            {"name": "US_SOCIAL_SECURITY_NUMBER"},
        ],
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0},
    }

    item = {"value": payload.data}

    response = dlp_client.inspect_content(request={
        "parent": project_path,
        "inspect_config": inspect_config,
        "item": item,
    })

    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append({
                "info_type": finding.info_type.name,
                "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                "quote": finding.quote,
            })
    return {"findings": findings, "full_response": str(response)}
