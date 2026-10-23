import os
from alibabacloud_alimt20181012 import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models


def translate_text(text, source_language, target_language):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    request = open_api_models.OpenApiRequest(
        {
            "SourceText": text,
            "SourceLanguage": source_language,
            "TargetLanguage": target_language,
        }
    )
    response = client.translate_general(request)
    return response.body.data.translated
