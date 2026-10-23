import os
import openai


def check_log_safety(log_text: str) -> dict:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=log_text, model="text-moderation-latest")
    result = response.results[0]
    categories = {
        cat: score for cat, score in result.category_scores.items() if score > 0.5
    }
    return {"flagged": result.flagged, "categories": categories}
