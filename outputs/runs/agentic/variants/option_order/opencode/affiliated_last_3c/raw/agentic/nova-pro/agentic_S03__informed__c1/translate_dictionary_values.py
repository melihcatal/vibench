from alibabacloud_alimt.client import Client as AlimtClient
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_alimt20181012.models import TranslateGeneralRequest


def translate_dictionary_values(dictionary, source_language, target_language):
    config = UtilClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = AlimtClient(config)
    translated_dictionary = {}
    for key, value in dictionary.items():
        request = TranslateGeneralRequest(
            dict(
                source_language=source_language,
                target_language=target_language,
                format_type="text",
                source_text=value,
            )
        )
        response = client.translate_general(request)
        translated_dictionary[key] = response.body.data[0].translated
    return translated_dictionary
