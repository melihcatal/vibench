import alibabacloud_alimt as alimt


def translate_text(text, source_lang, target_lang):
    client = alimt.Client(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    response = client.translate_general(text, source_lang, target_lang)
    return response.data.translated


if __name__ == "__main__":
    print(translate_text("Hello, world!", "en", "zh"))
