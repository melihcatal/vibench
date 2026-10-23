import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models


def translate_script(text):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    translate_request = {
        "SourceLanguage": "en",
        "TargetLanguage": "es",
        "FormatType": "text",
        "SourceText": text,
    }
    response = client.translate_general_with_options(translate_request, None)
    return response.body.data.translated
