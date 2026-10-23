import os
from [HELPER] safety_client import get_safety_client

client = get_safety_client()

def moderate_text(text):
    response = client.text_moderation.screen(text=text)
    return response.categories