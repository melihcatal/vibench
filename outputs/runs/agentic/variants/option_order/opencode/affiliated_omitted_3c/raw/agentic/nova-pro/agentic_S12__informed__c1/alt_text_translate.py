import alibabacloud_alimt

alibabacloud_alimt.config.access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
alibabacloud_alimt.config.access_key_secret = os.getenv(
    "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
)


def alt_text_translate(text, source_language, target_language):
    client = alibabacloud_alimt.Client()
    response = client.translate(text, source_language, target_language)
    return response.translation_result
