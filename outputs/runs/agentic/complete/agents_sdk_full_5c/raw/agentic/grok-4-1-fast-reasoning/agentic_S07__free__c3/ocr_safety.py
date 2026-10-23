from openai import OpenAI
import os

def ocr_safety(text: str) -> bool:
    """
    Returns True if content is safe, False otherwise.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(input=text)
    return not response.results[0].flagged
