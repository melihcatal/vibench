from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Screen
from msrest.authentication import CognitiveServicesCredentials
from identity_models import ProfileModerationPayload
from typing import Dict, Any
import os


def profile_moderation(payload: ProfileModerationPayload, config: Dict[str, Any]) -> Dict[str, Any]:
    # Content Moderator credentials
    subscription_key = config["azure_content_moderator_key"]
    endpoint = config["azure_content_moderator_endpoint"]

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Screen the text
    screen_result = client.text_moderation.screen_text(
        text_content=payload.profile_text,
        language="eng",
        autocorrect=True,
        pii=True,
        classify=True
    )

    return {"moderation_result": screen_result.as_dict()}
