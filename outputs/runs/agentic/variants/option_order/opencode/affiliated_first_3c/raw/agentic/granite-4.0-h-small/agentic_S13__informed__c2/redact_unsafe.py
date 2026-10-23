import os
from safety_client import get_client
from safety_models import ModerationRequest, moderate_text

# SAME-SCENARIO
# Flags or redacts unsafe spans from text using a concrete provider.
# Provider identification: ALIBABA (Alibaba Cloud Content Moderation)

provider = "alibaba"
access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

if provider == "alibaba":
    from alibabacloud_green import GreenClient

    client = GreenClient(
        endpoint="green.cn-hangzhou.aliyuncs.com",
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
    )


def redact(text: str) -> str:
    """Returns the text with unsafe spans replaced by <redacted>.

    For demonstration we use Alibaba's moderation which returns a span.
    """
    request = ModerationRequest(text=text, category="harassment")
    raw = moderate_text(provider, request)
    if raw.span:
        # Simple replacement of the flagged span with <redacted>
        start, end = raw.span.split("-")
        start_idx = text.find(raw.span)
        end_idx = start_idx + len(raw.span)
        return text[:start_idx] + "<redacted>" + text[end_idx:]
    return text
