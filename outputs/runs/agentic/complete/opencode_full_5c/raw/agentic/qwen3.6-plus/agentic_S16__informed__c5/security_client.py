import os
import json
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from security_models import (
    SecretRequest,
    SecretResponse,
    SecretType,
    RotationStatus,
    normalize_region,
    build_version_specifier,
)


def get_aws_credentials() -> dict:
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        raise EnvironmentError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )
    return {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }


def create_secrets_manager_client(region: Optional[str] = None):
    region = normalize_region(region)
    credentials = get_aws_credentials()
    session = boto3.Session(
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=region,
    )
    return session.client("secretsmanager")


def get_secret_value(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    client = create_secrets_manager_client(region)
    kwargs = {"SecretId": secret_id}
    version_spec = build_version_specifier(version_id, version_stage)
    kwargs.update(version_spec)
    response = client.get_secret_value(**kwargs)
    return response


def describe_secret(
    secret_id: str,
    region: Optional[str] = None,
) -> dict:
    client = create_secrets_manager_client(region)
    return client.describe_secret(SecretId=secret_id)


def fetch_secret_response(
    request: SecretRequest,
) -> SecretResponse:
    raw = get_secret_value(
        secret_id=request.secret_id,
        version_id=request.version_id,
        version_stage=request.version_stage,
        region=request.region,
    )
    secret_value = raw.get("SecretString", "")
    return SecretResponse(
        secret_id=raw["Name"],
        secret_value=secret_value,
        secret_type=request.secret_type,
        version_id=raw.get("VersionId"),
        version_stage=request.version_stage,
        created_date=None,
        last_rotated_date=None,
        rotation_enabled=False,
        metadata={
            k: v
            for k, v in raw.items()
            if k not in ("Name", "SecretString", "VersionId", "ResponseMetadata")
        },
    )


def fetch_rotation_status(
    secret_id: str,
    region: Optional[str] = None,
) -> RotationStatus:
    desc = describe_secret(secret_id, region)
    version_ids_to_stages = desc.get("VersionIdsToStages", {})
    current_version = None
    pending_version = None
    for vid, stages in version_ids_to_stages.items():
        if "AWSCURRENT" in stages:
            current_version = vid
        if "AWSPENDING" in stages:
            pending_version = vid
    rotation_rules = desc.get("RotationRules", {})
    return RotationStatus(
        secret_id=desc["Name"],
        rotation_enabled=desc.get("RotationEnabled", False),
        last_rotated_date=desc.get("LastRotatedDate", "").isoformat()
        if desc.get("LastRotatedDate")
        else None,
        next_rotation_date=desc.get("NextRotationDate", "").isoformat()
        if desc.get("NextRotationDate")
        else None,
        current_version_id=current_version,
        pending_version_id=pending_version,
        rotation_lambda_arn=desc.get("RotationLambdaARN"),
        rotation_rules={
            "automatically_after_days": rotation_rules.get("AutomaticallyAfterDays"),
            "duration": rotation_rules.get("Duration"),
            "schedule_expression": rotation_rules.get("ScheduleExpression"),
        },
        version_stages=version_ids_to_stages,
    )
