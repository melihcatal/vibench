from google.cloud import dlp_v2
from typing import List, Dict, Any

def redact_unsafe_content_with_google(text_content: str, project_id: str) -> Dict[str, Any]:
    dlp_client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"

    info_types_to_find = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"}
    ]

    try:
        response = dlp_client.inspect_content(
            request={
                "parent": parent,
                "inspect_config": {
                    "info_types": info_types_to_find,
                    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
                    "limits": {"max_findings_per_request": 0}
                },
                "item": {"value": text_content}
            }
        )
        
        findings = []
        if response.result and response.result.findings:
            for finding in response.result.findings:
                findings.append({
                    "info_type": finding.info_type.name,
                    "likelihood": finding.likelihood.name,
                    "quote": finding.quote
                })

        return {
            "original_content": text_content,
            "findings": findings,
            "redaction_info": "Findings reported. For full redaction, configure deidentify_content API.",
            "provider": "Google Cloud DLP"
        }

    except Exception as e:
        return {
            "error": str(e),
            "provider": "Google Cloud DLP"
        }

