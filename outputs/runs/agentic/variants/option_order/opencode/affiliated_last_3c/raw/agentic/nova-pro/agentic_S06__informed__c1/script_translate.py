from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_models
from alibabacloud_alimt20181012 import models as alimt_models


def translate_script(text):
    config = open_models.Config(
        access_key_id="your_access_key_id", access_key_secret="your_access_key_secret"
    )
    client = AlimtClient(config)
    translate_request = alimt_models.TranslateGeneralRequest(
        source_language="auto",
        target_language="en",
        format_type="text",
        source_text=text,
    )
    response = client.translate_general(translate_request)
    return response.body.data.translated
