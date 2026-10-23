from typing import Any


class SecurityModels:
    @staticmethod
    def normalize_response(response: Any) -> str:
        return response.payload.data.decode("UTF-8")
