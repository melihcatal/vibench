import os
from security_client import get_dlp_client, get_gcp_project_id
from security_models import DlpScanRequest, DlpScanResponse, DlpFinding
from google.cloud.dlp_v2 import types

def check_payload_safety(request: DlpScanRequest) -> DlpScanResponse:
    dlp_client = get_dlp_client()
    
    item = types.ContentItem(value=request.text)
    
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "LOCATION"},
        {"name": "PERSON_NAME"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "MEDICAL_TERM"},
        {"name": "GENERIC_ID"},
    ]
    
    inspect_config = types.InspectConfig(
        info_types=info_types,
        min_likelihood=types.Likelihood.POSSIBLE,
        limits=types.InspectConfig.FindingLimits(max_findings_per_request=100)
    )
    
    parent = f"projects/{request.project_id}"
    
    response = dlp_client.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )
    
    has_pii = False
    findings_list = []
    
    if response.result.findings:
        has_pii = True
        for finding in response.result.findings:
            findings_list.append(
                DlpFinding(
                    quote=finding.quote,
                    info_type=finding.info_type.name,
                    likelihood=types.Likelihood(finding.likelihood).name
                )
            )
            
    return DlpScanResponse(
        has_pii=has_pii,
        findings=findings_list
    )
