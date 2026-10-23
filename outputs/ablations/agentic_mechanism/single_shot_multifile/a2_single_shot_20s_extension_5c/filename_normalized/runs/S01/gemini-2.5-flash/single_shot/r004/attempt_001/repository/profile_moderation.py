import os
from azure.ai.contentmoderator import ContentModeratorClient
from azure.core.credentials import AzureKeyCredential
from identity_models import ModerationRequest
from typing import Dict, Any

def moderate_profile_text(request: ModerationRequest) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_MODERATOR_ENDPOINT")
    key = os.getenv("AZURE_MODERATOR_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_MODERATOR_ENDPOINT and AZURE_MODERATOR_KEY environment variables not set")

    client = ContentModeratorClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # The TextModerationClient is part of the newer package, ContentModeratorClient is the main client.
    # Using the raw text moderation method
    moderation_result = client.text_moderation.screen_text(text_content=request.text_content, content_type=request.text_type)
    
    # The response object can be complex, convert to dictionary for simpler return
    result_dict = moderation_result.as_dict() if hasattr(moderation_result, 'as_dict') else moderation_result.__dict__
    return result_dict
