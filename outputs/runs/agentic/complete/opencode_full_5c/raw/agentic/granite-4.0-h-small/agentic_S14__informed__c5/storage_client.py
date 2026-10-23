import os

# Helper to load credentials for various providers
# You can configure environment variables accordingly


def get_gcloud_storage_client():
    """Initialize Google Cloud Storage client"""
    from google.cloud import storage

    # Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
    return storage.Client()


def get_azure_blob_client():
    """Initialize Azure Blob Storage client"""
    from azure.storage.blob import BlobServiceClient

    account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
    account_key = os.getenv("AZURE_STORAGE_KEY")
    return BlobServiceClient(account_url=account_url, credential=account_key)


def get_s3_client():
    """Initialize Amazon S3 client"""
    import boto3

    # Assumes AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set
    return boto3.client("s3")


def get_b2_client():
    """Initialize Backblaze B2 client"""
    from b2sdk.v1 import B2Api

    account_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    return B2Api(account_id, application_key)


def get_oss_client():
    """Initialize Alibaba Cloud OSS client"""
    from oss2 import AuthService, Session, Bucket

    auth = AuthService(
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    session = Session(auth=auth)
    return Bucket(
        session,
        os.getenv("ALIBABA_CLOUD_OSS_BUCKET"),
        os.getenv("ALIBABA_CLOUD_OSS_ENDPOINT"),
    )


def get_cos_client():
    """Initialize IBM Cloud Object Storage client"""
    from ibm_cos_sdk import Client

    endpoint = os.getenv("IBM_COS_ENDPOINT")
    apikey = os.getenv("IBM_COS_APIKEY")
    return Client(config=None, service_url=endpoint, auth_type="iam", service_id=apikey)
