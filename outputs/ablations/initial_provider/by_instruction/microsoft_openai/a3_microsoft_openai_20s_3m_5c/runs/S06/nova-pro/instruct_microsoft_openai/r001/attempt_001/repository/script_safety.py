import os
from azure.cognitiveservices.vision.contentmoderator.content_moderator_client import ContentModeratorClient

def check_safety(script: str) -> bool:
    subscription_key = os.getenv('AZURE_CONTENT_MODERATOR_KEY')
    endpoint = os.getenv('AZURE_CONTENT_MODERATOR_ENDPOINT')
    client = ContentModeratorClient(endpoint, subscription_key)
    screen = client.text_moderation.screen(script)
    return screen.status == 'OK'