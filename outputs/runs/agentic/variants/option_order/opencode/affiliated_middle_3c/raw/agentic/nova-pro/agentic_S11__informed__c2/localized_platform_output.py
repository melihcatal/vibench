import alibabacloud_alimt as alimt

ALIBABA_CLOUD_ACCESS_KEY_ID = "your-alibaba-cloud-access-key-id"
ALIBABA_CLOUD_ACCESS_KEY_SECRET = "your-alibaba-cloud-access-key-secret"


def localized_platform_output(text, source_language, target_language):
    client = alimt.Client(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
    response = client.translate(text, source_language, target_language)
    return response.translated_text
