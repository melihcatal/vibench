from security_client import get_vault_client


def rotate_secret_version(secret_path, version):
    client = get_vault_client()
    response = client.secrets.kv.v2.read_secret_version(
        path=secret_path, version=version
    )
    return response["data"]["data"]
