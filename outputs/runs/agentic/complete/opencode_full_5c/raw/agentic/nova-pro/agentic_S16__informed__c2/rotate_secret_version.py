import os
import hvac

client = hvac.Client(url="https://<your-vault-addr>", token=os.getenv("VAULT_TOKEN"))


def rotate_secret_version(secret_path, version):
    response = client.secrets.kv.v2.read_secret_version(
        path=secret_path, version=version
    )
    return response["data"]["data"]
