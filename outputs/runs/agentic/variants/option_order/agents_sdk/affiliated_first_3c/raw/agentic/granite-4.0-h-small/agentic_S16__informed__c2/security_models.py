from typing import Dict, Any

class SecretPayload:
    """Normalized representation of a secret's plaintext data.",

    Attributes:
        json (Dict[str, Any]): Parsed JSON if the payload is JSON;
                               otherwise None.
        raw (str): The raw plaintext string returned by the secret store.
    """
    def __init__(self, raw: str):
        self.raw = raw
        try:
            self.json = json.loads(raw)
        except json.JSONDecodeError:
            self.json = None

class SecretMetadata:
    """Basic metadata extracted from the API response.",

    Attributes:
        name (str): Secret name/ID.
        created_at (str): ISO timestamp of creation.
        updated_at (str): ISO timestamp of last update.
        labels (list): List of labels attached to the secret.
    """
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.name = resp.get("name")
        self.created_at = resp.get("created_at")
        self.updated_at = resp.get("updated_at")
        self.labels = resp.get("labels", [])

# Helper to wrap an API response into friendly objects
def parse_secret_response(resp: Dict[str, Any]) -> tuple[SecretMetadata, SecretPayload]:
    meta = SecretMetadata(resp)
    payload = SecretPayload(resp.get("plaintext", ""))
    return meta, payload

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     # Assume we have a JSON secret stored under "my-json-secret"
#     raw_resp = get_secret("my-json-secret")  # from security_client.py
#     meta, payload = parse_secret_response(raw_resp)
#     print("Metadata:", meta.__dict__)
#     print("JSON payload:", payload.json)