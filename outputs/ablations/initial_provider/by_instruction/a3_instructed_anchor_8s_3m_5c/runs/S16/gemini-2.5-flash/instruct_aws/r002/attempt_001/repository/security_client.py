import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional

class AWSSecretsManagerClient:
    def __init__(self):
        self.client = boto3.client('secretsmanager')

    def get_secret(self, secret_name: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> Dict[str, Any]:
        try:
            kwargs = {'SecretId': secret_name}
            if version_id:
                kwargs['VersionId'] = version_id
            if version_stage:
                kwargs['VersionStage'] = version_stage
            
            get_secret_value_response = self.client.get_secret_value(**kwargs)
            return get_secret_value_response
        except ClientError as e:
            print(f"Error fetching secret {secret_name}: {e}")
            raise

    def list_secrets(self, max_results: int = 100) -> Dict[str, Any]:
        try:
            list_secrets_response = self.client.list_secrets(MaxResults=max_results)
            return list_secrets_response
        except ClientError as e:
            print(f"Error listing secrets: {e}")
            raise

    def update_secret_version_stage(self, secret_id: str, version_stage: str, secret_string: Optional[str] = None, secret_binary: Optional[bytes] = None) -> Dict[str, Any]:
        try:
            kwargs = {
                'SecretId': secret_id,
                'VersionStages': [version_stage]
            }
            if secret_string is not None:
                kwargs['SecretString'] = secret_string
            if secret_binary is not None:
                kwargs['SecretBinary'] = secret_binary

            update_secret_response = self.client.put_secret_value(**kwargs)
            return update_secret_response
        except ClientError as e:
            print(f"Error updating secret version stage for {secret_id}: {e}")
            raise
