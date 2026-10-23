import os
from openai import OpenAI

def check_live_caption_safety(caption_generator):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    client = OpenAI(api_key=api_key)
    for caption in caption_generator:
        if caption.strip():
            moderation = client.moderations.create(
                model='text-moderation-latest',
                input=caption
            )
            if not moderation.results[0].flagged:
                yield caption
            # Skip unsafe content
        else:
            yield caption