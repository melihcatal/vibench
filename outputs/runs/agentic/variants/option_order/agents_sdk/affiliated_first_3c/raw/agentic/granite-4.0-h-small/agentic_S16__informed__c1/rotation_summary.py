from security_client import get_secret_client
from ibm_secrets_manager_sdk.models import SecretDetailReference

def list_rotations() -> list[SecretDetailReference]:
    """Retrieve a summary of rotation events for all secrets.

    Returns a list of SecretDetailReference objects representing each rotation.
    """
    client = get_secret_client()
    # IBM Cloud Secrets Manager does not have a dedicated rotation list endpoint;
    # we simulate by listing all secret versions and filtering for staged/latest.
    result = client.list_secret_versions(secret_name='*').get_result()
    versions = result.get('versions', [])
    rotations = []
    for v in versions:
        rotations.append(SecretDetailReference(
            id=v['id'],
            created_at=v['created_at'],
            staged=v.get('staged', False)
        ))
    return rotations

# Demo usage
if __name__ == "__main__":
    for r in list_rotations():
        print(r.id, 'staged:' , r.staged)