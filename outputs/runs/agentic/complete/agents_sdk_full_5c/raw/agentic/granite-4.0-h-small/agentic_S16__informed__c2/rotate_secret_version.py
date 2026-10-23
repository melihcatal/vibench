import os
from dotenv import load_dotenv

# Alibaba Cloud KMS Secrets Manager example (managed secret store)
load_dotenv()  # loads .env if present
INSTANCE_ID = os.getenv('ALIBABA_KMS_INSTANCE_ID')
SECRET_NAME = os.getenv('ALIBABA_KMS_SECRET_NAME')
STAGED_VERSION = os.getenv('ALIBABA_KMS_STAGED_VERSION')  # e.g., 'staged'

# Using Alibaba Cloud SDK (alibabacloud_kms)
from alibabacloud_kms20201214.client import Client as KmsClient
from alibabacloud_tea_openapi.models import Config
from alibabacloud_kms20201214.models import GetSecretValueRequest

# Configure Alibaba Cloud client using credentials from environment
access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
region = os.getenv('ALIBABA_CLOUD_REGION', 'cn-hangzhou')
config = Config(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret,
    region_id=region,
)
client = KmsClient(config)

def rotate_secret_version():
    """
    Retrieve a specific staged version of a secret from Alibaba Cloud KMS Secrets Manager.
    Returns the secret payload as a string.
    """
    request = GetSecretValueRequest()
    request.secret_name = SECRET_NAME
    request.version_stage = STAGED_VERSION  # e.g., 'staged', 'current', etc.
    request_instance_id = INSTANCE_ID
    response = client.get_secret_value(request)
    # The SDK returns a response object; the secret is in response.secret_data (base64)
    import base64
    return base64.b64decode(response.secret_data).decode('UTF-8')
