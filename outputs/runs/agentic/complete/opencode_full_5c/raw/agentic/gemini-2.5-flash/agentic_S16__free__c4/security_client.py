import boto3
import json
from typing import Optional, Dict, Any


class SecretsManagerClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("secretsmanager", region_name=region_name)

    def get_secret(
        self,
        secret_name: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            if version_id:
                response = self.client.get_secret_value(
                    SecretId=secret_name, VersionId=version_id
                )
            elif version_stage:
                response = self.client.get_secret_value(
                    SecretId=secret_name, VersionStage=version_stage
                )
            else:
                response = self.client.get_secret_value(SecretId=secret_name)

            if "SecretString" in response:
                return (
                    json.loads(response["SecretString"])
                    if self._is_json(response["SecretString"])
                    else response["SecretString"]
                )
            else:
                return response["SecretBinary"]
        except Exception as e:
            print(f"Error retrieving secret '{secret_name}': {e}")
            raise

    def _is_json(self, value: str) -> bool:
        try:
            json.loads(value)
            return True
        except ValueError:
            return False

    def list_secrets(self) -> Dict[str, Any]:
        try:
            response = self.client.list_secrets()
            return response
        except Exception as e:
            print(f"Error listing secrets: {e}")
            raise

    def describe_secret(self, secret_name: str) -> Dict[str, Any]:
        try:
            response = self.client.describe_secret(SecretId=secret_name)
            return response
        except Exception as e:
            print(f"Error describing secret '{secret_name}': {e}")
            raise

    def update_secret_version_stage(
        self,
        secret_id: str,
        version_stage: str,
        move_from_version_id: str,
        move_to_version_id: str,
    ):
        try:
            response = self.client.update_secret_version_stage(
                SecretId=secret_id,
                VersionStage=version_stage,
                MoveFromVersionId=move_from_version_id,
                MoveToVersionId=move_to_version_id,
            )
            return response
        except Exception as e:
            print(f"Error updating secret version stage for '{secret_id}': {e}")
            raise
