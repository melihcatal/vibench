import os
from alibabacloud_green20180509 import Client as GreenClient
from alibabacloud_green20180509.models import AuthenticateContentRequest
from alibabacloud_tea_util.models import RuntimeOptions


def redact_unsafe(text):
    auth_request = AuthenticateContentRequest()
    auth_request.text_list = [text]
    client = GreenClient(
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    response = client.authenticate_content_with_options(auth_request, RuntimeOptions())
    redacted_text = response.body.data[0].censor_result.censor_text
    return redacted_text
