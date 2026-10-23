from google.cloud import dlp_v2
import os
from typing import List, Dict

def check_secret_label_safety(
    project_id: str,
    text_to_inspect: str,
    info_types: List[str] = None,
    min_likelihood: dlp_v2.Likelihood = dlp_v2.Likelihood.POSSIBLE,
) -> Dict[str, Any]:
    """
    Checks secret labels and notes for unsafe text using Google Cloud DLP API.
    Detects sensitive information like PII, credentials, etc.
    """
    if info_types is None:
        info_types = [
            "CREDIT_CARD_NUMBER",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER",
            "IP_ADDRESS",
            "GENERIC_CREDENTIALS", # Specific to DLP
            "AUTH_TOKEN", # Specific to DLP
        ]

    dlp = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"

    # Configure the inspection request
    item = {"value": text_to_inspect}
    inspect_config = {
        "info_types": [{"name": info_type} for info_type in info_types],
        "min_likelihood": min_likelihood,
        "include_quote": True,
    }

    # Perform the inspection
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
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
        "text_inspected": text_to_inspect,
        "findings": findings,
        "has_sensitive_data": bool(findings)
    }

