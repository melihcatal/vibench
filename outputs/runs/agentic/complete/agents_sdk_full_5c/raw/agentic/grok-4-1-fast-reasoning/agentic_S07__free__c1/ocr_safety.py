import openai
import os

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def ocr_safety(text: str) -> dict:
    """
    Check extracted document text for unsafe content.
    """
    response = client.moderations.create(
        model='text-moderation-latest',
        input=text
    )
    return response.results[0]
