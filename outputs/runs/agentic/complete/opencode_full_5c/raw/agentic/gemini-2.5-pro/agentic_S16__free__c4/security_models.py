from dataclasses import dataclass


@dataclass
class SecretRequest:
    """
    A request model for secret operations.
    """

    secret_id: str
    project_id: str


@dataclass
class SecretResponse:
    """
    A response model for secret operations.
    """

    secret_id: str
    payload: str
