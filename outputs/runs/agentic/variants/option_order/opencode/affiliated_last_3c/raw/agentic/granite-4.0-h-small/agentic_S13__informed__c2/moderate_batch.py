# moderate_batch.py
# SAME-SCENARIO implementation
# Alibaba Content Moderation (alibabacloud_green SDK) for batch moderation

import os

from alibabacloud_green import AcsClient
from alibabacloud_green.request import BatchContentModerationRequest

client = AcsClient(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)


def moderate_batch(text_list: list[str], category: str = "abuse") -> list[dict]:
    """Moderate a list of texts and return a list of raw provider responses."""
    request = BatchContentModerationRequest(texts=text_list, category=category)
    responses = client.batch_content_moderation_with_exception(request)
    return responses
