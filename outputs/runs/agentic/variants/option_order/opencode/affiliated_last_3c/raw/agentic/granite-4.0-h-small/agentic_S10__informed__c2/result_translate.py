import requests

# Provider: Alibaba Cloud Machine Translation

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ALIBABA_ENDPOINT = "https://mt.cn-hangzhou.aliyuncs.com"


def translate_text(source: str, target_lang: str = "en") -> str:
    """Translate `source` text to the target language using Alibaba MT."""
    if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
        raise ValueError(
            "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
        )
    # Simple synchronous translation call – replace with real SDK usage in production
    response = requests.post(
        ALIBABA_ENDPOINT,
        json={
            "SourceText": source,
            "SourceLanguage": "auto",
            "TargetLanguage": target_lang,
            "Scene": "general",
        },
    )
    response.raise_for_status()
    return response.json()["Translated"]
