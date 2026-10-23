import os
from [HELPER] safety_client import get_safety_client

client = get_safety_client()

def moderate_batch(texts):
    responses = client.text_moderation.batch_screen(texts=texts)
    return [{'text': text, 'decision': response.decision} for text, response in zip(texts, responses)]