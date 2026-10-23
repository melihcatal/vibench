import os
import boto3
import openai
from google.cloud import translate_v3 as translate

class SecurityClientConfig:
    _kms_client = None
    _cloudtrail_client = None
    _comprehend_client = None
    _openai_client = None
    _gcp_translate_client = None

    @staticmethod
    def get_aws_region() -> str:
        return os.environ.get("AWS_REGION", "us-east-1")

    @staticmethod
    def get_kms_encryption_key_id() -> str:
        key_id = os.environ.get("KMS_ENCRYPTION_KEY_ID")
        if not key_id:
            raise ValueError("KMS_ENCRYPTION_KEY_ID environment variable not set.")
        return key_id

    @staticmethod
    def get_kms_signing_key_id() -> str:
        key_id = os.environ.get("KMS_SIGNING_KEY_ID")
        if not key_id:
            raise ValueError("KMS_SIGNING_KEY_ID environment variable not set.")
        return key_id

    @staticmethod
    def get_openai_api_key() -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        return api_key

    @staticmethod
    def get_gcp_project_id() -> str:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")
        return project_id

    @classmethod
    def get_kms_client(cls):
        if cls._kms_client is None:
            cls._kms_client = boto3.client("kms", region_name=cls.get_aws_region())
        return cls._kms_client

    @classmethod
    def get_cloudtrail_client(cls):
        if cls._cloudtrail_client is None:
            cls._cloudtrail_client = boto3.client("cloudtrail", region_name=cls.get_aws_region())
        return cls._cloudtrail_client

    @classmethod
    def get_comprehend_client(cls):
        if cls._comprehend_client is None:
            cls._comprehend_client = boto3.client("comprehend", region_name=cls.get_aws_region())
        return cls._comprehend_client

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            cls._openai_client = openai.OpenAI(api_key=cls.get_openai_api_key())
        return cls._openai_client

    @classmethod
    def get_gcp_translate_client(cls):
        if cls._gcp_translate_client is None:
            cls._gcp_translate_client = translate.TranslationServiceClient()
        return cls._gcp_translate_client