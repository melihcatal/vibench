from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models

config = open_api_models.Config(
    access_key_id="your-access-key-id", access_key_secret="your-access-key-secret"
)

client = AlimtClient(config)


def translate_text(text, source_language, target_language):
    translate_general_request = alimt_models.TranslateGeneralRequest(
        source_language=source_language,
        target_language=target_language,
        format_type="text",
        source_text=text,
    )
    response = client.translate_general(translate_general_request)
    return response.body.data.translated


def welcome_translate(text):
    return translate_text(text, "en", "es")
