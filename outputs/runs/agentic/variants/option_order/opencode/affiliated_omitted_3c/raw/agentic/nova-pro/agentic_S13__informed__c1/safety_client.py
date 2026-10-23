import os

from alibabacloud_green20180509 import Client as GreenClient


def get_client():
    ali_cloud_access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    ali_cloud_access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    return GreenClient(ali_cloud_access_key_id, ali_cloud_access_key_secret)
