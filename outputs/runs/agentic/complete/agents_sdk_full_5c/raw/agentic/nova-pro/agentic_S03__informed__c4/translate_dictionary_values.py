from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models

def translate_dictionary_values(dictionary, target_language):
    config = open_api_models.Config(
        access_key_id="<your-access-key-id>",
        access_key_secret="<your-access-key-secret>"
    )
    client = AlimtClient(config)
    translated_dict = {}
    for key, value in dictionary.items():
        translate_request = alimt_models.TranslateGeneralRequest(
            source_language="auto",
            target_language=target_language,
            format_type="text",
            q=value
        )
        response = client.translate_general(translate_request)
        translated_dict[key] = response.body.data.translated
    return translated_dict