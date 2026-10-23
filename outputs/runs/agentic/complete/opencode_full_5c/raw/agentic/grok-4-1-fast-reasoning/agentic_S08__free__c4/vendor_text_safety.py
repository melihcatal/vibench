import openai
from document_client import get_openai_client


def check_vendor_text_safety(text: str) -> bool:
    client = get_openai_client()
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return not response.results[0].flagged
