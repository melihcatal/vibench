import argparse
from datetime import datetime
from typing import Dict, Any, List
from security_models import FetchResponse, normalize_secret, LabelMetadata, check_label_safety
from security_client import get_secret

# Mapping of provider IDs to short names (used for summary output)
PROVIDER_NAMES = {
    'azure': 'Azure Key Vault',
    'aws': 'AWS Secrets Manager',
    'google': 'Google Secret Manager'
}


def summarize_secret_rotation(secret_name: str, provider: str, vault_url: str = None, region: str = None) -> Dict[str, Any]:
    """
    Fetch the latest secret version, normalize payload, inspect rotation metadata,
    and return a concise rotation status summary.
    """
    # Retrieve raw secret using configured client (provider logic in security_client)
    raw = get_secret(provider, secret_name)
    # Normalize regardless of provider
    normalized: Dict[str, Any] = normalize_secret(raw)
    # Extract labels if present
    labels: LabelMetadata = normalized.get('labels', {})
    # Perform safety check on labels
    unsafe = check_label_safety(labels)
    # Build summary dictionary
    summary = {
        'provider': PROVIDER_NAMES.get(provider, 'Unknown'),
        'vault': vault_url or region,
        'secret_name': secret_name,
        'version': normalized.get('version'),
        'fetched_at': datetime.utcnow().isoformat() + 'Z',
        'value_type': 'json' if isinstance(normalized.get('value'), dict) else 'string',
        'unsafe_labels': unsafe
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description='Rotate and summarize a secret.')
    parser.add_argument('--provider', choices=['azure', 'aws', 'google'], default='azure', help='Secret manager provider')
    parser.add_argument('--vault-url', help='Azure vault URL (required for Azure)')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default us-east-1)')
    parser.add_argument('secret_name', help='Name/ID of the secret to rotate/summarize')
    args = parser.parse_args()

    summary = summarize_secret_rotation(args.secret_name, args.provider, args.vault_url, args.region)
    # Pretty-print as JSON
    import json
    print(json.dumps(summary, indent=2, default=str))

if __name__ == '__main__':
    main()
