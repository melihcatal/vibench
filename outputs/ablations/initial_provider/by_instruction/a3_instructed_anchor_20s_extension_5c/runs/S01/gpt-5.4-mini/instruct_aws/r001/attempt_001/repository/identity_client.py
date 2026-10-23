import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class IdentityConfig:
    user_pool_id: str
    client_id: str
    aws_region: str
    support_table_name: str
    support_bucket: str


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        user_pool_id=os.environ["AWS_COGNITO_USER_POOL_ID"],
        client_id=os.environ["AWS_COGNITO_APP_CLIENT_ID"],
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        support_table_name=os.getenv("AWS_DYNAMODB_SUPPORT_TABLE", "onboarding-support"),
        support_bucket=os.getenv("AWS_S3_SUPPORT_BUCKET", "onboarding-support-bucket"),
    )


def cognito_idp_client():
    return boto3.client("cognito-idp", region_name=load_identity_config().aws_region)


def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=load_identity_config().aws_region)


def s3_client():
    return boto3.client("s3", region_name=load_identity_config().aws_region)
