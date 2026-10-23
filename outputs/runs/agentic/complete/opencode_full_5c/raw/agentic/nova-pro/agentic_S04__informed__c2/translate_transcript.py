import os
from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models

ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

config = open_api_models.Config(
    access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
)
client = AlimtClient(config)


def translate_transcript(text):
    request = {
        "SourceLanguage": "en",
        "TargetLanguage": "es",
        "FormatType": "text",
        "SourceText": text,
    }
    response = client.translate_general(request)
    return response.body.data.translated


if __name__ == "__main__":
    print(translate_transcript("Hello, world!"))
