import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models

config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)

client = AlimtClient(config)


def translate(text, source_language, target_language):
    translate_general_request = {
        "SourceLanguage": source_language,
        "TargetLanguage": target_language,
        "FormatType": "text",
        "SourceText": text,
    }
    runtime = {"timeout": 10000}
    try:
        response = client.translate_general_with_options(
            translate_general_request, runtime
        )
        return response.body.data.translated
    except Exception as e:
        print(e)
