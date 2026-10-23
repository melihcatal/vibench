import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, Any, Optional
from security_models import SecretResponse


class SecurityClient:
    def __init__(self, region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")):
        self.region = region
        self.client = boto3.client("secretsmanager", region_name=region)

    def get_secret(
        self, secret_name: str, version_stage: Optional[str] = None
    ) -> SecretResponse:
        try:
            kwargs: Dict[str, Any] = {"SecretId": secret_name}
            if version_stage is not None:
                kwargs["VersionStage"] = version_stage
            response = self.client.get_secret_value(**kwargs)
            secret_string = response["SecretString"]
            return SecretResponse(
                value=secret_string,
                version_id=response["VersionId"],
                version_stages=response["VersionStages"],
                created_date=response.get("CreatedDate"),
            )
        except (ClientError, NoCredentialsError) as e:
            raise RuntimeError(
                f"Failed to retrieve secret '{secret_name}' in region '{self.region}': {str(e)}"
            )
