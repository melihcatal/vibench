import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models


def translate(text, source_lang, target_lang):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    translate_request = alimt_models.TranslateGeneralRequest(
        source_language=source_lang,
        target_language=target_lang,
        format_type="text",
        source_text=text,
    )
    response = client.translate_general(translate_request)
    return response.body.data[0].translated


if __name__ == "__main__":
    print(translate("Hello, world!", "en", "es"))
