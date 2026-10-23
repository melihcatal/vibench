import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient

def check_safety(script: str) -> bool:
    subscription_key = os.getenv('AZURE_CONTENT_MODERATOR_KEY')
    endpoint = os.getenv('AZURE_CONTENT_MODERATOR_ENDPOINT')
    client = ContentModeratorClient(endpoint, subscription_key)
    result = client.text_moderation.screen(script)
    return result.is_safe