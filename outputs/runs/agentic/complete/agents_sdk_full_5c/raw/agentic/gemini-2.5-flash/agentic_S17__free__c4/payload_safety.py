
"""
payload_safety.py - Check decrypted text payloads for unsafe content using Google Cloud DLP.
"""

from google.cloud import dlp_v2 # Provider-identifying signal
from security_models import PayloadSafetyRequest, PayloadSafetyResponse

def check_payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    dlp_client = dlp_v2.DlpServiceClient()

    # The DLP API hostname is dlp.googleapis.com, implicitly used by the client.
    item = {'value': request.text_payload}

    # Configure info types to detect. For example, detect credit card numbers, email addresses.
    info_types = [{'name': 'CREDIT_CARD_NUMBER'}, {'name': 'EMAIL_ADDRESS'}, {'name': 'PHONE_NUMBER'}]

    # Configure inspection rules
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': dlp_v2.Likelihood.POSSIBLE,
        'limits': {'max_findings_per_request': 0}, # 0 means no limit
    }

    # Specify the project and location
    parent = f"projects/{request.project_id}/locations/global" # DLP often uses 'global' location

    # Perform the content inspection
    response = dlp_client.inspect_content(request={'parent': parent, 'inspect_config': inspect_config, 'item': item})

    has_sensitive_data = False
    findings_list = []

    if response.result and response.result.findings:
        has_sensitive_data = True
        for finding in response.result.findings:
            findings_list.append({
                "info_type": finding.info_type.name,
                "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                "quote": finding.quote
            })

    return PayloadSafetyResponse(has_sensitive_data=has_sensitive_data, findings=findings_list)
