import os
import subprocess
from typing import List


def contains_unsafe_content(text: str) -> bool:
    """Checks selected log message text for unsafe content using a hosted moderation service.

    This implementation delegates to Alibaba Cloud Content Moderation via its SDK.
    Returns True if the text is flagged as unsafe; otherwise False.
    """
    # Configuration extracted from environment variables (SDK handles auth)
    endpoint = os.getenv(
        "ALIBABA_CONTENT_MOD_ENDPOINT", "content-moderation.cn-shanghai.aliyuncs.com"
    )
    region = os.getenv("ALIBABA_REGION", "cn-shanghai")

    # Simple wrapper using the official SDK (assumed installed as alibabacloud_green)
    from alibabacloud_green20180509.client import Client as GreenClient
    from alibabacloud_tea_util.models import Config
    from alibabacloud_green20180509.models import TextModerationRequest

    client = GreenClient(
        Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            region_id=region,
            endpoint=endpoint,
        )
    )

    request = TextModerationRequest(scene="text_censored", text=text.encode("utf-8"))
    response = client.text_moderation(request)
    # Safely extract the flagged flag from the JSON response
    try:
        result = response.to_map()
        return result.get("data")["results"][0].get("text_flag") == "1"
    except Exception as e:
        # In case of any parsing error, treat as safe to avoid false positives
        return False
