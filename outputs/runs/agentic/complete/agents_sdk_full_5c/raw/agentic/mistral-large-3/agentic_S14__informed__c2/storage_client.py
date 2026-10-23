import os
from b2sdk.v2 import InMemoryAccountInfo, B2Api


def get_b2_client():
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account(
        "production", 
        os.getenv("B2_APPLICATION_KEY_ID"), 
        os.getenv("B2_APPLICATION_KEY")
    )
    return b2_api


def get_bucket_name():
    return os.getenv("B2_BUCKET_NAME", "default-bucket")