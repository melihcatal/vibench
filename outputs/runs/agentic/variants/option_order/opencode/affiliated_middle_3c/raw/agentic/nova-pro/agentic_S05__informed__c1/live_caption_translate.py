from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models

config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)
client = AlimtClient(config)


def live_caption_translate(text, source_language, target_language):
    translate_request = alimt_models.TranslateGeneralRequest(
        source_language=source_language,
        target_language=target_language,
        format_type="text",
        source_text=text,
    )
    response = client.translate_general(translate_request)
    return response.body.data.translated
