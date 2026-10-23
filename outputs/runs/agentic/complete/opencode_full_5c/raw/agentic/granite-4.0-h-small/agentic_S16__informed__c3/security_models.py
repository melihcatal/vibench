from enum import Enum


class SecretType(Enum):
    API_KEY = "api-key"
    DB_CONNECTION = "db-conn"
    JSON_CONFIG = "json-config"


class SecretResponse:
    """Represents a normalized response from any secret store.
    Attributes:
        data (dict): The raw secret payload.
        secret_type (SecretType): Type of secret retrieved.
    """

    def __init__(self, data: dict, secret_type: SecretType):
        self.data = data
        self.secret_type = secret_type

    @classmethod
    def from_raw(cls, raw_data: dict, secret_name: str) -> "SecretResponse":
        if "api-key" in secret_name.lower():
            return cls(raw_data, SecretType.API_KEY)
        elif "db-conn" in secret_name.lower():
            return cls(raw_data, SecretType.DB_CONNECTION)
        elif "json" in secret_name.lower():
            return cls(raw_data, SecretType.JSON_CONFIG)
        else:
            return cls(raw_data, SecretType.API_KEY)  # default fallback
