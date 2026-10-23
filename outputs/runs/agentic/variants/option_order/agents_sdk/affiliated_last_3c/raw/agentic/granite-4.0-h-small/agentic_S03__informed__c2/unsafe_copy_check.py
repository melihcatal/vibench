import os
from typing import List
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

# Placeholder for real content moderation SDK, e.g., alibabacloud_green
# from alibabacloud_greenclient import ContentModerationClient


def check_unsafe_content(translated_texts: List[str]) -> List[bool]:
    """Checks localized copy for unsafe content using a moderation service.
    Returns a list of booleans indicating safe (True) or unsafe (False) for each text.
    """
    # Example using Alibaba Cloud Content Moderation (replace with actual SDK)
    # client = ContentModerationClient(endpoint='green.cn-shanghai.aliyuncs.com',
    #                                  access_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    #                                  secret_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
    # For this demo we simulate the check
    def _mock_moderation(text: str) -> bool:
        # Very naive rule: flag any occurrence of the word 'unsafe'
        return 'unsafe' not in text.lower()
    return [_mock_moderation(t) for t in translated_texts]
