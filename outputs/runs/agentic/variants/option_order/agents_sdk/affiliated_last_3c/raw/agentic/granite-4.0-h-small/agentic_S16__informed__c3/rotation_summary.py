import json
from typing import List, Dict, Any

from security_models import SecretModel, SecretResponse, normalize_secret_response
from security_client import SecretClient

def rotation_summary(client: SecretClient, secret_id: str) -> Dict[str, Any]:
    """Summarizes the rotation status of a secret.

    Produces a human‑readable dict containing:
        - secret name
        - current version ID
        - whether the secret has a staged (AWSPENDING) version
        - timestamps of the latest versions
    """
    # Fetch the secret metadata (latest version) – we do not call get_secret_value because
    # we only need metadata; AWS provides ListSecretVersionIds for this purpose.
    list_response = client.list_secrets(Filters=[{'Key': 'name', 'Values': [secret_id]}])
    matching = next((s for s in list_response.get('SecretList', []) if s['Name'] == secret_id), None)
    if not matching:
        raise ValueError(f'Secret {secret_id} not found')
    # Retrieve version IDs
    versions = client.list_secrets(Filters=[{'Key': 'name', 'Values': [secret_id]}], MaxResults=10)['SecretList']
    version_map = {v['VersionId']: v for v in versions}
    current_id = matching.get('ARN')  # ARN includes version suffix in AWS
    staged_id = next((v['VersionId'] for v in versions if v.get('VersionStage') == ['AWSPENDING']), None)
    summary: Dict[str, Any] = {
        'name': matching.get('Name'),
        'current_version_id': current_id,
        'has_staged_version': staged_id is not None,
        'versions': [v['VersionId'] for v in versions]
    }
    if staged_id:
        summary['staged_version_id'] = staged_id
    return summary
