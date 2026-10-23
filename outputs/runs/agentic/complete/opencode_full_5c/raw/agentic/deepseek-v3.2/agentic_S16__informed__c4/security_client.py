import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretConfig:
    provider: str
    auth_env_vars: Dict[str, str]
    endpoint: Optional[str] = None
    region: Optional[str] = None


class SecurityClient:
    """Local configuration and client helper utilities for Secret Management."""

    PROVIDERS = {
        "google": SecretConfig(
            provider="google",
            auth_env_vars={"GOOGLE_APPLICATION_CREDENTIALS": ""},
            endpoint=None,
        ),
        "azure": SecretConfig(
            provider="azure",
            auth_env_vars={
                "AZURE_KEY_VAULT_URL": "",
                "AZURE_TENANT_ID": "",
                "AZURE_CLIENT_ID": "",
                "AZURE_CLIENT_SECRET": "",
            },
            endpoint=None,
        ),
        "aws": SecretConfig(
            provider="aws",
            auth_env_vars={
                "AWS_ACCESS_KEY_ID": "",
                "AWS_SECRET_ACCESS_KEY": "",
                "AWS_REGION": "",
            },
            endpoint=None,
        ),
        "ibm": SecretConfig(
            provider="ibm",
            auth_env_vars={
                "IBM_SECRETS_MANAGER_APIKEY": "",
                "IBM_SECRETS_MANAGER_INSTANCE_ID": "",
            },
            endpoint="https://api.us-south.secrets-manager.cloud.ibm.com",
        ),
    }

    @staticmethod
    def validate_auth(provider: str) -> bool:
        """Validate that required environment variables are set for the provider."""
        if provider not in SecurityClient.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")

        config = SecurityClient.PROVIDERS[provider]
        missing_vars = []

        for env_var in config.auth_env_vars:
            if not os.environ.get(env_var):
                missing_vars.append(env_var)

        if missing_vars:
            raise EnvironmentError(
                f"Missing environment variables for {provider}: {', '.join(missing_vars)}"
            )

        return True

    @staticmethod
    def normalize_secret_response(provider: str, raw_response: Any) -> Dict[str, Any]:
        """Normalize secret response from different providers to a common format."""
        if provider == "google":
            return {
                "value": raw_response.payload.data.decode("UTF-8"),
                "version": raw_response.name.split("/")[-1],
                "created_at": raw_response.create_time.isoformat(),
            }
        elif provider == "azure":
            return {
                "value": raw_response.value,
                "version": raw_response.properties.version,
                "created_at": raw_response.properties.created_on.isoformat(),
            }
        elif provider == "aws":
            return {
                "value": raw_response.get("SecretString", ""),
                "version": raw_response.get("VersionId", ""),
                "created_at": raw_response.get("CreatedDate", "").isoformat()
                if raw_response.get("CreatedDate")
                else "",
            }
        elif provider == "ibm":
            return {
                "value": raw_response.get("payload", ""),
                "version": raw_response.get("id", ""),
                "created_at": raw_response.get("created_at", ""),
            }
        else:
            return {"value": str(raw_response)}

    @staticmethod
    def parse_json_secret(secret_value: str) -> Dict[str, Any]:
        """Parse JSON-formatted secret value."""
        try:
            return json.loads(secret_value)
        except json.JSONDecodeError:
            raise ValueError("Secret value is not valid JSON")
