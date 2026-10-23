import os
import openai

# Load configuration from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError('Set OPENAI_API_KEY environment variable')

openai.api_key = api_key

def moderate_text(user_text: str, unsafe_categories=('hate','harassment','self_harm','sexual','violence')):
    """Use OpenAI Moderation endpoint to score text for policy violations.
    Returns a dict with category scores, each ranging 0.0-1.0.
    """
    response = openai.Moderation.create(input=user_text)
    # response['results'] is a list with one element
    result = response['results'][0]
    # Filter only requested categories
    scores = {cat: result['categories'][cat] for cat in unsafe_categories if cat in result['categories']}
    return scores
