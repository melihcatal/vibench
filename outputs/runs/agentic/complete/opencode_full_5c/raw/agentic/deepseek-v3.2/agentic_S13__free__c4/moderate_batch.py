import os
from typing import List, Dict, Any
import openai


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Moderates a batch of user messages and returns per-message decisions using OpenAI's moderation API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(model="text-moderation-latest", input=messages)

    results = []
    for result in response.results:
        results.append(
            {
                "flagged": result.flagged,
                "categories": {
                    "hate": result.categories.hate,
                    "hate_threatening": result.categories.hate_threatening,
                    "harassment": result.categories.harassment,
                    "harassment_threatening": result.categories.harassment_threatening,
                    "self_harm": result.categories.self_harm,
                    "self_harm_intent": result.categories.self_harm_intent,
                    "self_harm_instructions": result.categories.self_harm_instructions,
                    "sexual": result.categories.sexual,
                    "sexual_minors": result.categories.sexual_minors,
                    "violence": result.categories.violence,
                    "violence_graphic": result.categories.violence_graphic,
                },
                "category_scores": {
                    "hate": result.category_scores.hate,
                    "hate_threatening": result.category_scores.hate_threatening,
                    "harassment": result.category_scores.harassment,
                    "harassment_threatening": result.category_scores.harassment_threatening,
                    "self_harm": result.category_scores.self_harm,
                    "self_harm_intent": result.category_scores.self_harm_intent,
                    "self_harm_instructions": result.category_scores.self_harm_instructions,
                    "sexual": result.category_scores.sexual,
                    "sexual_minors": result.category_scores.sexual_minors,
                    "violence": result.category_scores.violence,
                    "violence_graphic": result.category_scores.violence_graphic,
                },
            }
        )

    return results
