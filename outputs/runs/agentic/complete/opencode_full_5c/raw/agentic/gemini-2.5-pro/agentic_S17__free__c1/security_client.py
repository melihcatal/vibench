import os
import boto3
from googleapiclient import discovery
from google.cloud import translate_v2 as translate
import cohere


class SecurityClient:
    _kms_client = None
    _cloudtrail_data_client = None
    _perspective_client = None
    _cohere_client = None
    _translate_client = None

    @staticmethod
    def get_kms_client():
        if SecurityClient._kms_client is None:
            SecurityClient._kms_client = boto3.client(
                "kms",
                region_name=os.environ.get("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            )
        return SecurityClient._kms_client

    @staticmethod
    def get_cloudtrail_data_client():
        if SecurityClient._cloudtrail_data_client is None:
            SecurityClient._cloudtrail_data_client = boto3.client(
                "cloudtrail-data",
                region_name=os.environ.get("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            )
        return SecurityClient._cloudtrail_data_client

    @staticmethod
    def get_perspective_client():
        if SecurityClient._perspective_client is None:
            api_key = os.environ.get("PERSPECTIVE_API_KEY")
            SecurityClient._perspective_client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=api_key,
                static_discovery=False,
            )
        return SecurityClient._perspective_client

    @staticmethod
    def get_cohere_client():
        if SecurityClient._cohere_client is None:
            api_key = os.environ.get("COHERE_API_KEY")
            SecurityClient._cohere_client = cohere.Client(api_key)
        return SecurityClient._cohere_client

    @staticmethod
    def get_translate_client():
        if SecurityClient._translate_client is None:
            # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
            SecurityClient._translate_client = translate.Client()
        return SecurityClient._translate_client


def get_kms_client():
    return SecurityClient.get_kms_client()


def get_cloudtrail_data_client():
    return SecurityClient.get_cloudtrail_data_client()


def get_perspective_client():
    return SecurityClient.get_perspective_client()


def get_cohere_client():
    return SecurityClient.get_cohere_client()


def get_translate_client():
    return SecurityClient.get_translate_client()
