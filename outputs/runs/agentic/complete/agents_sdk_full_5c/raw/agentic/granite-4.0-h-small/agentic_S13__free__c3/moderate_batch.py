import os
import openai
from typing import List, Dict

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError('Set OPENAI_API_KEY environment variable')
openai.api_key = api_key

def moderate_batch(texts: List[str], unsafe_categories=('hate','harassment','self_harm','sexual','violence')):
    """Moderate a batch of messages using OpenAI's moderation API.
    Returns a list of per-message dicts containing category scores.
    """
    batch = []
    for text in texts:
        resp = openai.Moderation.create(input=text)
        result = resp['results'][0]
        scores = {cat: result['categories'][cat] for cat in unsafe_categories if cat in result['categories']}
        batch.append(scores)
    return batch
