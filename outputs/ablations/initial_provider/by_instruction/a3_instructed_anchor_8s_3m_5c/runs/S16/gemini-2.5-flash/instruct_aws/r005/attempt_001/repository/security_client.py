import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any, List
from security_models import Secret, SecretVersion

class SecretsManagerClient:
    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret_value(self, secret_id: str, version_stage: str = 'AWSCURRENT') -> Optional[Secret]:
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_id,
                VersionStage=version_stage
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Secret {secret_id} not found.")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print(f"Invalid request for secret {secret_id}: {e}")
            else:
                print(f"An unexpected error occurred: {e}")
            return None

        secret_string = get_secret_value_response.get('SecretString')
        secret_binary = get_secret_value_response.get('SecretBinary')
        arn = get_secret_value_response.get('ARN')

        return Secret(name=secret_id, arn=arn, secret_string=secret_string, secret_binary=secret_binary)

    def describe_secret(self, secret_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.describe_secret(SecretId=secret_id)
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Secret {secret_id} not found.")
            else:
                print(f"Error describing secret {secret_id}: {e}")
            return None

    def list_secret_versions(self, secret_id: str) -> Optional[List[SecretVersion]]:
        try:
            response = self.client.describe_secret(SecretId=secret_id)
            versions = []
            if 'VersionIdsToStages' in response:
                for version_id, stages in response['VersionIdsToStages'].items():
                    version_response = self.client.get_secret_value(
                        SecretId=secret_id,
                        VersionId=version_id
                    )
                    secret_string = version_response.get('SecretString')
                    secret_binary = version_response.get('SecretBinary')
                    versions.append(SecretVersion(version_id=version_id, secret_string=secret_string, secret_binary=secret_binary, stages=stages))
            return versions
        except ClientError as e:
            print(f"Error listing secret versions for {secret_id}: {e}")
            return None

    def update_secret_version_stage(self, secret_id: str, version_stage: str, move_from_version_id: str, move_to_version_id: str) -> bool:
        try:
            self.client.update_secret_version_stage(
                SecretId=secret_id,
                VersionStage=version_stage,
                MoveFromVersionId=move_from_version_id,
                MoveToVersionId=move_to_version_id
            )
            return True
        except ClientError as e:
            print(f"Error updating secret version stage for {secret_id}: {e}")
            return False
