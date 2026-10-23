import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models


def translate_dictionary_values(dictionary, source_lang, target_lang):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    translated_dict = {}
    for key, value in dictionary.items():
        translate_request = alimt_models.TranslateGeneralRequest(
            source_language=source_lang,
            target_language=target_lang,
            format_type="text",
            source_text=value,
        )
        response = client.translate_general(translate_request)
        translated_dict[key] = response.body.data[0].translated
    return translated_dict


if __name__ == "__main__":
    print(
        translate_dictionary_values(
            {"greeting": "Hello, world!", "question": "How are you?"}, "en", "es"
        )
    )
