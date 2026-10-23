import openai
import os


def moderate_free_text_claims_or_notes(text: str):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    return response.results[0]
