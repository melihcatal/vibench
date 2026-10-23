# secret_label_safety.py
# [LATER-STEP]
# Check secret labels and notes for unsafe text (AWS Secrets Manager)
import json
from security_models import SecretLabelSafetyRequest, SecretLabelSafetyResponse
from security_client import get_secret_manager_client

client = get_secret_manager_client()

def check_labels_for_secret(secret_name: str, labels: Dict[str, str], notes: str | None = None) -> SecretLabelSafetyResponse:
    """Retrieve secret metadata and run unsafe-keyword detection.",
    # Some providers expose labels via a dedicated describe call; mimic with tags here
    describe_resp = client.describe_secret(SecretId=secret_name)
    secret_labels = describe_resp.get('Tags', [])
    # Map tags to dict for uniform handling
    tag_dict = {tag['Key']: tag['Value'] for tag in secret_labels}
    request: SecretLabelSafetyRequest = {
        'secret_id': secret_name,
        'labels': tag_dict,
        'notes': notes,
    }
    return check_secret_labels(request)

# Helper from security_models (reuse)
from security_models import check_secret_labels as _check_secret_labels

if __name__ == '__main__':
    # Example usage: assume a secret called 'my-api-key' with some tags
    result = check_labels_for_secret('my-api-key', labels={'env': 'prod', 'owner': 'team-a'}, notes='Password: s3cr3t!')
    print(json.dumps(result, indent=2))
