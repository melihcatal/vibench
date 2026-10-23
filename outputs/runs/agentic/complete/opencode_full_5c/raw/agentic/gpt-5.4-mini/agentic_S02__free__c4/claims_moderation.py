import openai
import os


def moderate_claims(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0]
