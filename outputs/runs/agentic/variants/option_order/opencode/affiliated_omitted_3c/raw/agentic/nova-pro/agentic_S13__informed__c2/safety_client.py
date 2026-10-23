import os
from alibabacloud_green20180509 import Client as GreenClient
from alibabacloud_green20180509.models import AuthenticateContentRequest
from alibabacloud_tea_util.models import RuntimeOptions


def create_client():
    return GreenClient(
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
