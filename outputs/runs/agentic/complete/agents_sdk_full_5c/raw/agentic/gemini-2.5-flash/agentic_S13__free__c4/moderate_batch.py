import openai
import os

def moderate_batch_messages(texts: list[str]) -> list[dict]:
    # Ensure OPENAI_API_KEY is set in environment
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(input=texts)
    
    results = []
    for i, moderation_result in enumerate(response.results):
        results.append({
            "text": texts[i],
            "flagged": moderation_result.flagged,
            "categories": {k: v for k, v in moderation_result.categories.model_dump().items()},
            "category_scores": {k: v for k, v in moderation_result.category_scores.model_dump().items()},
        })
    return results
