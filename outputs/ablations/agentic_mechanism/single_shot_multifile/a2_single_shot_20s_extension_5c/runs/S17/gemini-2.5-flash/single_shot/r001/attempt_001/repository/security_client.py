import os
import boto3
from google.cloud import kms_v1, translate_v2
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
import openai
import cohere
import json

class SecurityClients:
    _aws_kms_client = None
    _gcp_kms_client = None
    _azure_key_vault_client = None
    _openai_client = None
    _cohere_client = None
    _gcp_translate_client = None
    _aws_cloudtrail_client = None

    @classmethod
    def get_aws_kms_client(cls):
        if cls._aws_kms_client is None:
            cls._aws_kms_client = boto3.client(
                'kms',
                region_name=os.environ.get('AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
            )
        return cls._aws_kms_client

    @classmethod
    def get_gcp_kms_client(cls):
        if cls._gcp_kms_client is None:
            # Ensure GOOGLE_APPLICATION_CREDENTIALS or gcloud auth is set up
            cls._gcp_kms_client = kms_v1.KeyManagementServiceClient()
        return cls._gcp_kms_client

    @classmethod
    def get_azure_key_vault_client(cls):
        if cls._azure_key_vault_client is None:
            vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
            if not vault_url:
                raise ValueError("AZURE_KEY_VAULT_URL environment variable is not set.")
            credential = DefaultAzureCredential()
            cls._azure_key_vault_client = KeyClient(vault_url=vault_url, credential=credential)
        return cls._azure_key_vault_client

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            cls._openai_client = openai
        return cls._openai_client

    @classmethod
    def get_cohere_client(cls):
        if cls._cohere_client is None:
            cohere_api_key = os.environ.get("COHERE_API_KEY")
            if not cohere_api_key:
                raise ValueError("COHERE_API_KEY environment variable is not set.")
            cls._cohere_client = cohere.Client(cohere_api_key)
        return cls._cohere_client

    @classmethod
    def get_gcp_translate_client(cls):
        if cls._gcp_translate_client is None:
            # Google Cloud Translation v2 requires GOOGLE_APPLICATION_CREDENTIALS or default auth
            cls._gcp_translate_client = translate_v2.Client()
        return cls._gcp_translate_client

    @classmethod
    def get_aws_cloudtrail_client(cls):
        if cls._aws_cloudtrail_client is None:
            cls._aws_cloudtrail_client = boto3.client(
                'cloudtrail',
                region_name=os.environ.get('AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
            )
        return cls._aws_cloudtrail_client