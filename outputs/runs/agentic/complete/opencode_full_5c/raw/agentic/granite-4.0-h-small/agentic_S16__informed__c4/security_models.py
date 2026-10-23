import typing as t


class SecretRequest:
    """Model for a request targeting a secret.

    Fields are generic and can be expanded per provider needs.
    """

    project_id: str
    secret_id: str
    version_id: str = "latest"

    def __init__(
        self, *, project_id: str, secret_id: str, version_id: str = "latest"
    ) -> None:
        self.project_id = project_id
        self.secret_id = secret_id
        self.version_id = version_id


class SecretResponse:
    """Normalized response model from a secret fetch operation.

    Encapsulates raw payload, metadata, and health information.
    """

    raw: str
    metadata: t.Dict[str, t.Any]
    error: bool = False

    def __init__(self, *, raw: str, metadata: t.Dict = None) -> None:
        self.raw = raw
        self.metadata = metadata if metadata is not None else {}
        self.error = not raw


# Helper to normalize provider-specific responses into this model
def normalize_response(provider_response: any) -> SecretResponse:
    if isinstance(provider_response, bytes):
        return SecretResponse(raw=provider_response.decode("utf-8"))
    elif isinstance(provider_response, str):
        return SecretResponse(raw=provider_response)
    else:
        raise TypeError("Unsupported response type")
