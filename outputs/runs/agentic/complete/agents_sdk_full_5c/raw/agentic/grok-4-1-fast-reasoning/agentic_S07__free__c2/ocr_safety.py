from openai import OpenAI
import os

def ocr_safety(text: str) -> bool:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return not response.results[0].flagged
