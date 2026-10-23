import openai
import os

def message_safety(text: str) -> bool:
    """
    Check message payload text for unsafe content
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError('OPENAI_API_KEY required')
    response = client.moderations.create(
        model='text-moderation-latest',
        input=text
    )
    return not response.results[0].flagged