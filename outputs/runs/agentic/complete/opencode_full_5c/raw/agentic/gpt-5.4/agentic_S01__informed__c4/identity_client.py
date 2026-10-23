import os
from typing import Optional

import boto3
from google.cloud import firestore
from google.cloud import translate_v2 as translate
from openai import OpenAI


COGNITO_PROVIDER = "amazon-cognito-idp"
TRANSLATE_PROVIDER = "google-cloud-translate"
MODERATION_PROVIDER = "commentanalyzer.googleapis.com"
OPENAI_PROVIDER = "openai"
FIRESTORE_PROVIDER = "google-cloud-firestore"
OPENAI_MODEL = "gpt-4.1-mini"


def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_cognito_client():
    return boto3.client("cognito-idp", region_name=get_aws_region())


def get_cognito_client_id() -> str:
    return getenv_required("COGNITO_CLIENT_ID")


def get_cognito_user_pool_id() -> str:
    return getenv_required("COGNITO_USER_POOL_ID")


def get_translate_client() -> translate.Client:
    return translate.Client()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=getenv_required("OPENAI_API_KEY"))


def get_perspective_api_key() -> str:
    return getenv_required("PERSPECTIVE_API_KEY")


def get_firestore_client(project: Optional[str] = None) -> firestore.Client:
    firestore_project = (
        project or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    )
    return firestore.Client(project=firestore_project)


def get_firestore_collection() -> str:
    return os.getenv("FIRESTORE_ONBOARDING_COLLECTION", "onboarding_profiles")
