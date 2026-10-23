from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_secret_label_safety(texts: list[str]) -> list[dict]:
    results = []
    for text in texts:
        response = client.moderations.create(
            model="text-moderation-4-2024-10-14",
            input=text
        )
        result = response.results[0]
        results.append({
            'flagged': result.flagged,
            'categories': result.categories,
            'category_scores': result.category_scores
        })
    return results