import openai
from document_client import Config


def ocr_safety(text: str) -> bool:
    client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return not response.results[0].flagged
