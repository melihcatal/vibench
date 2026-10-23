# alt_text_translate.py
"""Later-step integration: Translate generated image descriptions to another language.

Uses Alibaba Cloud Machine Translation SDK as the concrete provider (identifiable in code).
"""

from aliyun_tablestore import MTSClient
from aliyun_tablestore import StreamItem

# Provider identifiers (Alibaba Cloud Machine Translation)
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
MT_ENDPOINT = "mt.cn-hangzhou.aliyuncs.com"


def translate_caption(caption: str, target_lang: str = "zh") -> str:
    """Translate a short image caption to the target language.

    Args:
        caption: The source text (english or any language supported by MT).
        target_lang: ISO language code; default is Chinese (zh).

    Returns:
        Translated caption string.
    """
    client = MTSClient(
        region_id="cn-hangzhou",
        access_key_id=ALIBABA_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        endpoint=MT_ENDPOINT,
    )
    # Alibaba MT API expects a JSON payload with source text
    response = client.get_text_translation(
        source_text=caption,
        source_lang="en",
        target_lang=target_lang,
    )
    # The API returns a JSON with a .TranslatedText field (or similar)
    translated = response.get("TranslatedText", "")
    return translated.strip()
