from google.cloud import dlp_v2

def check_payload_safety(project_id: str, text_payload: str, info_types: list = None):
    dlp_client = dlp_v2.DlpServiceClient()

    if info_types is None:
        info_types = [
            {'name': 'EMAIL_ADDRESS'},
            {'name': 'PHONE_NUMBER'},
            {'name': 'CREDIT_CARD_NUMBER'},
            {'name': 'US_SOCIAL_SECURITY_NUMBER'},
            {'name': 'IP_ADDRESS'},
        ]

    # The inspect_content request
    item = {'value': text_payload}

    inspect_config = {
        'info_types': info_types,
        'min_likelihood': dlp_v2.Likelihood.POSSIBLE,
        'limits': {'max_findings_per_request': 0}
    }

    parent = f"projects/{project_id}/locations/global"

    response = dlp_client.inspect_content(
        request={'parent': parent, 'inspect_config': inspect_config, 'item': item}
    )

    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append({
                'quote': finding.quote,
                'info_type': finding.info_type.name,
                'likelihood': dlp_v2.Likelihood(finding.likelihood).name
            })

    return {'has_unsafe_content': bool(findings), 'findings': findings}
