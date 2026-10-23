import alibabacloud_alimt
import os

# Alibaba Cloud Machine Translation API
# Set your credentials in environment variables:
# ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
ALIMT_CLIENT = alibabacloud_alimt.AliMTClient(
    region_id="cn-hangzhou",
    access_key_id=os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
    access_key_secret=os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
)


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text using Alibaba Cloud Machine Translation."""
    response = ALIMT_CLIENT.translate(
        source_text=text, source_lang="auto", target_lang=target_lang
    )
    # The SDK returns a list of translated sentences; join them
    return " ".join(response.translated_text)


# Example usage (commented out)
# if __name__ == "__main__":
#     src = "Bonjour tout le monde"
#     print(f"Translated: {translate_text(src, target_lang='en')}")
