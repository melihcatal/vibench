import os
from typing import TypedDict

# Local helper: simplified configuration loader
SECRET_MANAGER_ENDPOINT = os.getenv(
    "SECRET_MANAGER_ENDPOINT", "https://secretsmanager.example.com"
)

# Typedefs for API responses
RequestPayload = TypedDict(
    "RequestPayload",
    {
        "secret_name": str,
        "optional_payload": dict,
    },
)
ResponsePayload = TypedDict(
    "ResponsePayload",
    {
        "value": str,
        "metadata": dict,
    },
)


class SecurityClient:
    @staticmethod
    def get_secret(secret_name: str) -> ResponsePayload:
        # Placeholder for real SDK call
        return {
            "value": f"secret-value-for-{secret_name}",
            "metadata": {"version": "1", "created_by": "admin"},
        }

    @staticmethod
    def rotate_secret(secret_name: str, payload: RequestPayload) -> ResponsePayload:
        # Placeholder for rotation logic
        return {
            "value": f"rotated-value-for-{secret_name}",
            "metadata": {
                "stage": payload.get("optional_payload", {}).get("stage", "DEFAULT")
            },
        }
