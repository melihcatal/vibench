import os
from typing import Dict, Any
from alibabacloud_green20220302.client import Client as GreenClient
from alibabacloud_green20220302.models import TextModerationRequest, TextModerationResponse
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

def check_prompt_safety(text: str) -> Dict[str, Any]:
    """
    Check text for unsafe content using Alibaba Cloud Content Moderation.
    
    Args:
        text: Input text to check.
    
    Returns:
        Moderation result as a dictionary.
    """
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    
    if not access_key_id or not access_key_secret:
        raise ValueError("Alibaba Cloud credentials not set.")
    
    config = util_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
    )
    client = GreenClient(config)
    
    request = TextModerationRequest(
        service="ai_moderation",
        service_parameters={
            "content": text,
            "scene": "antispam",
        }
    )
    
    try:
        response = client.text_moderation(request)
        return {
            "safe": response.body.result.suggestion == "pass",
            "details": response.body.result,
        }
    except Exception as e:
        return {"safe": False, "error": str(e)}}