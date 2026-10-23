import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_free_text_claims(text: str) -> dict:
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return {
        "flagged": response.results[0].flagged,
        "categories": response.results[0].categories,
        "category_scores": response.results[0].category_scores,
    }
