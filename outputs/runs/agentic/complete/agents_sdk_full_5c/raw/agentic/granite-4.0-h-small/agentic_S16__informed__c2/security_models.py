from typing import Dict, Any, Union

# Normalized request model for fetching any secret
FetchRequest = Dict[str, Any]

# Normalized response model from any provider
FetchResponse = Union[Dict[str, Any], str]

# Secret label metadata model (used for safety checks)
LabelMetadata = Dict[str, Any]

# Helper to normalize different provider payloads into a common shape
# Expected fields: value (the secret payload), version (current version id), created_at (timestamp), labels (optional)

def normalize_secret(payload: FetchResponse) -> Dict[str, Any]:
    if isinstance(payload, dict):
        # Azure Key Vault response example: {'value': 'secret', 'id': 'url', 'version': 'ver', ...}
        # AWS response example: {'SecretString': json_string, 'VersionId': 'abc'}
        # Google response example: {'payload': {'data': json_string}}
        normalized = {
            'value': None,
            'version': None,
            'created_at': None,
            'labels': []
        }
        if 'value' in payload:  # Azure
            normalized['value'] = payload['value']
            normalized['version'] = payload.get('version')
            normalized['created_at'] = payload.get('attributes', {}).get('created')
            normalized['labels'] = payload.get('tags', {})
        elif 'SecretString' in payload:  # AWS
            import json
            secret_json = json.loads(payload['SecretString']) if payload['SecretString'] else {}
            normalized['value'] = secret_json.get('username')  # example field
            normalized['version'] = payload.get('VersionId')
            normalized['created_at'] = payload.get('CreatedDate')
            normalized['labels'] = payload.get('Tags', [])
        elif 'payload' in payload:  # Google
            import json
            data = json.loads(payload['payload']['data'])
            normalized['value'] = data
            normalized['version'] = payload.get('name').split('/')[-1]  # crude version extraction
            normalized['created_at'] = payload.get('createTime')
            normalized['labels'] = payload.get('labels', {})
        else:
            raise ValueError('Unknown payload structure')
    else:
        # Assume payload is raw secret string (e.g., from a simple REST API)
        normalized = {'value': payload, 'version': None, 'created_at': None, 'labels': []}
    return normalized

# Safety filter for secret label / note content
UNSAFE_TERMS = ['password', 'passphrase', 'secret', 'apikey', 'token']


from typing import List

def check_label_safety(labels: LabelMetadata) -> List[str]:
    """
    Scan label keys and values for unsafe terms.
    Returns a list of offending term strings.
    """
    offenses = []
    if isinstance(labels, dict):
        for key, val in labels.items():
            for term in UNSAFE_TERMS:
                if term in key.lower() or term in str(val).lower():
                    offenses.append(f"Label '{key}' contains unsafe term '{term}'")
    return offenses

# Example usage (guarded)
if __name__ == '__main__':
    test_labels = {
        'env': 'prod',
        'owner': 'team-a',
        'note': 'Contains a password123 for testing'
    }
    print('Offenses:', check_label_safety(test_labels))
