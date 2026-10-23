import os
from alibabacloud_alimt.client import Client as AlimtClient
from alibabacloud_tea_util.client import Client as UtilClient


def get_translation_client():
    config = UtilClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    return AlimtClient(config)
