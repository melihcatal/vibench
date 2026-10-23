import os
from [HELPER] safety_client import get_safety_client

client = get_safety_client()

def safety_threshold(text, thresholds):
    response = client.text_moderation.screen(text=text)
    for category, score in response.scores.items():
        if score > thresholds.get(category, 0):
            return False
    return True