import os
from typing import Any, Dict

import boto3

from identity_models import normalize_email, normalize_locale, normalize_profile_text


AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", "")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "")
S3_BUCKET_NAME = os.getenv("ONBOARDING_NOTES_BUCKET", "")
TRANSLATE_ARN = os.getenv("AWS_TRANSLATE_LAMBDA_ARN", "")
COMPREHEND_MODEL_ARN = os.getenv("AWS_COMPREHEND_ENDPOINT_ARN", "")


def cognito_idp_client():
    return boto3.client("cognito-idp", region_name=AWS_REGION)


def cognito_identity_client():
    return boto3.client("cognito-identity", region_name=AWS_REGION)


def s3_client():
    return boto3.client("s3", region_name=AWS_REGION)


def translate_client():
    return boto3.client("translate", region_name=AWS_REGION)


def comprehend_client():
    return boto3.client("comprehend", region_name=AWS_REGION)


def config() -> Dict[str, str]:
    return {
        "region": AWS_REGION,
        "user_pool_id": COGNITO_USER_POOL_ID,
        "client_id": COGNITO_CLIENT_ID,
        "bucket_name": S3_BUCKET_NAME,
        "translate_arn": TRANSLATE_ARN,
        "comprehend_model_arn": COMPREHEND_MODEL_ARN,
    }


def prepare_identity_payload(email: str, password: str) -> Dict[str, str]:
    return {"email": normalize_email(email), "password": password}


def prepare_locale_payload(locale: str, text: str) -> Dict[str, str]:
    return {"locale": normalize_locale(locale), "text": normalize_profile_text(text)}
