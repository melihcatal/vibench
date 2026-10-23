from typing import TypedDict


# Request model for fetching secrets
class FetchSecretRequest(TypedDict):
    secret_name: str
    secret_type: str  # e.g., 'arbitrary', 'username_password'


# Response model for fetching secrets
class FetchSecretResponse(TypedDict):
    metadata: dict
    secret_data: dict


# Normalization helpers (extend as needed)
NORMALIZE_PAYLOAD = {
    "api_key": lambda v: v.strip(),
    "db_conn": lambda v: v,
}


def normalize_request(req: FetchSecretRequest) -> FetchSecretRequest:
    """Sanitize request fields.
    Currently ensures string types and trims API keys.
    """
    if req["secret_type"] == "api_key":
        req["secret_name"] = req["secret_name"].strip()
    return req


# Example usage (in a later step)
if __name__ == "__main__":
    example_req = {
        "secret_name": "my-api-key",
        "secret_type": "api_key",
    }
    norm = normalize_request(example_req)
    print("Normalized request:", norm)
