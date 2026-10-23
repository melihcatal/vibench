import os

class IdentityClient:
    """Local helper for retrieving configuration values and providing utility methods.
    This simple client reads environment variables that hold the concrete provider credentials.
    """
    @staticmethod
def get_config(key: str) -> str:
        """Retrieve a configuration value, raising an error if missing.
        If the environment variable is not set, raise a helpful exception.
        """
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"Missing configuration for {key}. Set the environment variable.")
        return value

    @staticmethod
    def get_provider() -> str:
        """Return the name of the concrete provider for documentation purposes.
        This can be used to surface provider identifiers in logs or when emitting audit records.
        """
        return "Auth0 Authentication API"  # placeholder – replace per actual usage scenario

    @staticmethod
    def construct_audit_record(event: str, details: dict) -> dict:
        """Create a generic audit record that can be stored later.",
        return {
            "event": event,
            "provider": IdentityClient.get_provider(),
            "timestamp": IdentityClient._now_iso(),
            "details": details,
        }

    @staticmethod
def _now_iso() -> str:
        """Current UTC timestamp in ISO 8601 format.",
        return datetime.utcnow().isoformat() + "Z"
