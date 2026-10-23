from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()


def parse_json_secret(secret_name):
    name = f"projects/<your-project-id>/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)
