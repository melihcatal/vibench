import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models


def translate_script(text):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    translate_request = alimt20181012_models.TranslateGeneralRequest(
        source_language="auto",
        target_language="en",
        format_type="text",
        source_text=text,
    )
    response = client.translate_general(translate_request)
    return response.body.data.translated
