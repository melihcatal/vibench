from typing import Any, Dict


# Security Models Helper
class SecretResponse:
    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SecretResponse":
        return SecretResponse(data["value"])
