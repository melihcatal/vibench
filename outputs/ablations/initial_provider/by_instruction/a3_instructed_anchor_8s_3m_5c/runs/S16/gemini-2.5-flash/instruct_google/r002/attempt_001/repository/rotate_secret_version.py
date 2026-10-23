import os
from security_client import SecurityClient

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    client = SecurityClient()
    secret_payload = client.access_secret_version(project_id, secret_id, version_id)
    return secret_payload.data.decode('utf-8')

def create_new_secret_version(project_id: str, secret_id: str, new_payload: str) -> str:
    client = SecurityClient()
    new_version_name = client.create_secret_version(project_id, secret_id, new_payload.encode('utf-8'))
    return new_version_name

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_to_rotate_id = "my-rotatable-secret"
    # Read the latest version
    # latest_secret = rotate_secret_version(project_id, secret_to_rotate_id)
    # print(f"Latest secret version content: {latest_secret}")

    # Simulate creating a new version
    # new_secret_content = "new_secret_value_" + os.urandom(4).hex()
    # new_version = create_new_secret_version(project_id, secret_to_rotate_id, new_secret_content)
    # print(f"Created new secret version: {new_version}")
