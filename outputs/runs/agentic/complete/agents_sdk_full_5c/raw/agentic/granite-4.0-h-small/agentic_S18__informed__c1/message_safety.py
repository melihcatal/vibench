import os
from typing import Dict

# Using OpenAI's content filter (via the openai Python SDK) as the safety check
# Provider identified by the import name 'openai'

try:
    from openai import OpenAI
except ImportError:
    raise ImportError('Please install the openai package: pip install openai')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise RuntimeError('Set the OPENAI_API_KEY environment variable')

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = 'gpt-4o-mini'  # concrete model identifier

def check_safety(message_payload: Dict[str, str]) -> bool:
    """Run the OpenAI Moderation endpoint on message text and return True if safe.

    Args:
        message_payload (Dict[str, str]): Expected to contain a key 'text' with the raw content.

    Returns:
        bool: True when the content is classified as safe, False otherwise.
    """
    text = message_payload.get('text', '')
    if not text:
        return True  # nothing to check
    response = client.moderations.create(model=MODEL, input=text)
    categories = response.flagged  # Boolean per category (e.g., hate, self_harm, sexual)
    # Consider the content unsafe if any category is flagged
    unsafe = any(categories.values())
    if unsafe:
        print('Unsafe content detected:', categories)
    return not unsafe


def main():
    sample = {'text': 'Buy cheap viagra now!!!', 'user_id': '123'}
    safe = check_safety(sample)
    print('Message safe:', safe)

if __name__ == '__main__':
    main()
