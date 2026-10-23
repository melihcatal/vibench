import os
import json
from ibm_key_protect_sdk import KmsApiV2


# IBM Key Protect client helper (already defined in security_client)
class KeyManagementClient:
    _instance = None

    @staticmethod
    def _create_client() -> KmsApiV2:
        return KmsApiV2(
            url=os.getenv("IBM_KEY_PROTECT_URL"),
            api_key=os.getenv("IBM_KEY_PROTECT_APIKEY"),
        )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance


def key_usage_summary() -> dict:
    """Summarize key usage and crypto events by listing all keys and their operation counts.

    Returns a dictionary mapping key IDs to a summary of usage information.
    """
    client = KeyManagementClient()
    try:
        # List keys call is illustrative; actual IBM Key Protect does not expose a bulk usage list
        # Here we simulate by calling the list_keys endpoint if available
        response = client.list_keys()  # type: ignore[attr-defined]
        keys = response.get_result().get("keys", [])
        summary = {}
        for k in keys:
            key_id = k["id"]
            # Placeholder values; a real implementation would query audit logs
            summary[key_id] = {
                "operations": 0,
                "last_used": None,
                "status": k.get("status"),
            }
        return summary
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve key usage: {e}")


# Example usage when run as script
if __name__ == "__main__":
    summary = key_usage_summary()
    print(json.dumps(summary, indent=2))
