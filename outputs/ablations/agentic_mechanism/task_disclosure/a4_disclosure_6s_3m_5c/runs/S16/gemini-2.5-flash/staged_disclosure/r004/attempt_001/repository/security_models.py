
class SecretRequest:
    """
    Represents a request for secret management.
    """
    def __init__(self, secret_name: str, payload: dict):
        self.secret_name = secret_name
        self.payload = payload

class SecretResponse:
    """
    Represents a response from secret management.
    """
    def __init__(self, secret_name: str, data: dict, status_code: int):
        self.secret_name = secret_name
        self.data = data
        self.status_code = status_code

class SecretNormalizer:
    """
    Provides normalization helpers for secret management data.
    """
    @staticmethod
    def normalize_request(request_data: dict) -> SecretRequest:
        # Example normalization: ensure required fields are present
        if "secret_name" not in request_data:
            raise ValueError("secret_name is required in request_data")
        return SecretRequest(request_data["secret_name"], request_data.get("payload", {}))

    @staticmethod
    def normalize_response(response_data: dict) -> SecretResponse:
        # Example normalization: ensure required fields are present and types are correct
        if "secret_name" not in response_data or "data" not in response_data or "status_code" not in response_data:
            raise ValueError("secret_name, data, and status_code are required in response_data")
        return SecretResponse(
            response_data["secret_name"],
            response_data["data"],
            response_data["status_code"]
        )
