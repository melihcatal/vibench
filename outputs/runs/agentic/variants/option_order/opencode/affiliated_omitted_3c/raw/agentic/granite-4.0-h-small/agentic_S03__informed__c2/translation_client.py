import os
from typing import Optional

# Example: Alibaba Cloud Machine Translation configuration
# Uses environment variables for authentication

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ALIBABA_ENDPOINT = "mt.cn-hangzhou.aliyuncs.com"

# Helper to build Alibaba Cloud Translation client
from alibabacloud_alimt20200323.client import Client


def get_alimt_client() -> Client:
    """Create and return a configured Alibaba Cloud Translation client."""
    return Client(
        access_key_id=ALIBABA_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        endpoint=ALIBABA_ENDPOINT,
    )


# Placeholder for other providers – left empty as a location for future implementations
# e.g., def get_deepl_client(): ...  # DEEPL_AUTH_KEY
# e.g., def get_google_client(): ...  # GOOGLE_APPLICATION_CREDENTIALS

# Simple utility to pick a client based on an env var name map
PROVIDER_CLIENT_MAPPERS = {
    "ALIBABA_CLOUD_ACCESS_KEY_ID": get_alimt_client,
    # "DEEPL_AUTH_KEY": get_deepl_client,
    # "GOOGLE_APPLICATION_CREDENTIALS": get_google_client,
    # "AZURE_TRANSLATOR_KEY": get_azure_client,
    # "AWS_ACCESS_KEY_ID": get_amazon_client,
}

# Example helper to translate using the Alibaba client


def translate_with_alimt(
    source_text: str, source_lang: str = "en", target_lang: str = "zh"
) -> str:
    client = get_alimt_client()
    response = client.mt_translate(
        {
            "SourceText": source_text,
            "SourceLanguage": source_lang,
            "TargetLanguage": target_lang,
            "Category": "general",
        }
    )
    return response.get("TargetText", "Translation failed")


# Example usage when run directly (demonstrates Alibaba usage)
if __name__ == "__main__":
    if ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET:
        sample = "Hello, world!"
        print(f"Original: {sample}")
        print(f"Translated (Alibaba): {translate_with_alimt(sample)}")
    else:
        print("Alibaba credentials not set. Skipping demo.")
