from observability_client import GcpObservabilityClient
from google.cloud.dlp_v2 import types

def metric_annotation_safety(payload, config=None):
    config = config or {}
    project_id = config.get('gcp_project_id')
    text_to_check = payload['annotation_text']

    client = GcpObservabilityClient().dlp_client

    # The parent project ID is required for DLP API calls.
    parent = f"projects/{project_id}"

    # Configure the content to inspect.
    item = types.ContentItem(value=text_to_check)

    # Configure the types of info to look for.
    # Using a broad set for general safety, can be customized.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "GENERIC_PERSON_NAME"},
    ]

    # Configure the inspection request.
    inspect_config = types.InspectConfig(
        info_types=info_types,
        min_likelihood=types.Likelihood.POSSIBLE,
        include_quote=True # To get the actual detected text
    )

    # Perform the inspection.
    response = client.inspect_content(request={'parent': parent, 'inspect_config': inspect_config, 'item': item})

    findings = []
    if response.result.findings:
        for finding in response.result.findings:
            findings.append({
                'info_type': finding.info_type.name,
                'likelihood': types.Likelihood(finding.likelihood).name,
                'quote': finding.quote
            })

    is_safe = not bool(findings)

    return {'is_safe': is_safe, 'findings': findings}
