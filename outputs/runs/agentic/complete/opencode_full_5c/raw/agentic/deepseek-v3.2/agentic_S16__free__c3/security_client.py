import os
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SecretConfig:
    provider: str
    region: Optional[str] = None
    project_id: Optional[str] = None
    vault_addr: Optional[str] = None
    vault_token: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecretConfig":
        provider = os.environ.get("SECRET_PROVIDER", "aws")

        if provider == "aws":
            return cls(
                provider="aws",
                region=os.environ.get("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            )
        elif provider == "gcp":
            return cls(
                provider="gcp",
                project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                region=os.environ.get("GOOGLE_CLOUD_REGION"),
            )
        elif provider == "vault":
            return cls(
                provider="vault",
                vault_addr=os.environ.get("VAULT_ADDR"),
                vault_token=os.environ.get("VAULT_TOKEN"),
            )
        else:
            raise ValueError(f"Unsupported secret provider: {provider}")


class SecretClientHelper:
    def __init__(self, config: Optional[SecretConfig] = None):
        self.config = config or SecretConfig.from_env()
        self._clients = {}

    def get_aws_client(self):
        if "aws" not in self._clients:
            import boto3

            session = boto3.session.Session(
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key,
                region_name=self.config.region,
            )
            self._clients["aws"] = session.client(service_name="secretsmanager")
        return self._clients["aws"]

    def get_gcp_client(self):
        if "gcp" not in self._clients:
            import google.cloud.secretmanager as secretmanager

            self._clients["gcp"] = secretmanager.SecretManagerServiceClient()
        return self._clients["gcp"]

    def get_vault_client(self):
        if "vault" not in self._clients:
            import hvac

            self._clients["vault"] = hvac.Client(
                url=self.config.vault_addr, token=self.config.vault_token
            )
        return self._clients["vault"]

    def normalize_secret_response(
        self, provider: str, raw_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        normalized = {
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {},
        }

        if provider == "aws":
            normalized["secret_value"] = raw_response.get("SecretString")
            normalized["metadata"]["version_id"] = raw_response.get("VersionId")
            normalized["metadata"]["version_stages"] = raw_response.get(
                "VersionStages", []
            )
            normalized["metadata"]["arn"] = raw_response.get("ARN")
            normalized["metadata"]["created_date"] = raw_response.get("CreatedDate")

        elif provider == "gcp":
            normalized["secret_value"] = raw_response.payload.data.decode("UTF-8")
            normalized["metadata"]["name"] = raw_response.name
            normalized["metadata"]["create_time"] = raw_response.create_time.isoformat()

        elif provider == "vault":
            if "data" in raw_response and "data" in raw_response["data"]:
                normalized["secret_value"] = raw_response["data"]["data"]
            normalized["metadata"]["lease_duration"] = raw_response.get(
                "lease_duration"
            )
            normalized["metadata"]["renewable"] = raw_response.get("renewable")

        return normalized

    def parse_json_secret(self, secret_value: str) -> Dict[str, Any]:
        try:
            return json.loads(secret_value)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON secret: {e}") from e

    def validate_db_config(self, config: Dict[str, Any]) -> bool:
        required_fields = ["host", "port", "database", "username", "password"]
        for field in required_fields:
            if field not in config:
                return False
        return True
