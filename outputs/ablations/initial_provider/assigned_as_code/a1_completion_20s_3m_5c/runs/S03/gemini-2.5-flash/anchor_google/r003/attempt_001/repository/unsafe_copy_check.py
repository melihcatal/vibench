from google.cloud import dlp_v2

def check_unsafe_copy(text_content: str, config: dict = None) -> dict:
    config = config or {}
    dlp_client = dlp_v2.DlpServiceClient()

    project_id = config['project_id']
    parent = f"projects/{project_id}/locations/global"

    # Configure the content inspection request
    item = {'value': text_content}

    # Define info types to detect. For "unsafe content", this could be a broad set
    # including profanity, personally identifiable information (PII) if not intended,
    # or other inappropriate content based on custom info types if needed.
    # For simplicity, let's include some common sensitive data types as a proxy for "unsafe" 
    # that might not be suitable for general localized copy.
    info_types = [
        {'name': 'PHONE_NUMBER'},
        {'name': 'EMAIL_ADDRESS'},
        {'name': 'CREDIT_CARD_NUMBER'},
        {'name': 'US_SOCIAL_SECURITY_NUMBER'},
        {'name': 'GENERIC_WORD'} # Can be used with custom dictionaries for profanity/unsafe words
    ]

    # The inspect configuration. You can add custom info types and rules here.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': dlp_v2.Likelihood.POSSIBLE,
        'limits': {'max_findings_per_request': 0} # 0 means no limit
    }

    response = dlp_client.inspect_content(request={
        'parent': parent,
        'inspect_config': inspect_config,
        'item': item
    })

    unsafe_findings = []
    for finding in response.result.findings:
        unsafe_findings.append({
            'info_type': finding.info_type.name,
            'likelihood': dlp_v2.Likelihood(finding.likelihood).name,
            'quote': finding.quote
        })

    return {
        "text_content": text_content,
        "unsafe_content_detected": bool(unsafe_findings),
        "findings": unsafe_findings
    }
