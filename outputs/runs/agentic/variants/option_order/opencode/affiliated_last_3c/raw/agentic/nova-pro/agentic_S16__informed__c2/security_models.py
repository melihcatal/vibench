from typing import Any


# Define local request, response, and normalization helpers for Secret Management
class SecretResponse:
    def __init__(self, value: Any):
        self.value = value
