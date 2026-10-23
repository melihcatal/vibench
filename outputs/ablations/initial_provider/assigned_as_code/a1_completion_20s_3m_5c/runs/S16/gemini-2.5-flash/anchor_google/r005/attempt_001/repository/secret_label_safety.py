import os

from google.cloud import dlp_v2

def secret_label_safety_check(project_id: str, text_to_inspect: str, info_types: list = None) -> dict:
    dlp_client = dlp_v2.DlpServiceClient()

    if info_types is None:
        info_types = [
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
            {"name": "IP_ADDRESS"},
            {"name": "AUTH_TOKEN"},
            {"name": "US_SOCIAL_SECURITY_NUMBER"},
            {"name": "DATE_OF_BIRTH"}
        ]

    item = {"value": text_to_inspect}

    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0}
    }

    parent = f"projects/{project_id}/locations/global"

    response = dlp_client.inspect_content(request={
        "parent": parent,
        "inspect_config": inspect_config,
        "item": item
    })

    findings_summary = []
    if response.result.findings:
        for finding in response.result.findings:
            findings_summary.append({
                "info_type": finding.info_type.name,
                "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                "quote": finding.quote
            })

    return {"text_inspected": text_to_inspect, "findings": findings_summary}
