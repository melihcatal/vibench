import os
from openai import OpenAI
from typing import Dict, Any, Optional


def moderate_text(text: str) -> Dict[str, Any]:
    """
    Score user text for unsafe or policy-violating content using OpenAI's moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": {
            "hate": result.categories.hate,
            "hate/threatening": result.categories.hate_threatening,
            "harassment": result.categories.harassment,
            "harassment/threatening": result.categories.harassment_threatening,
            "self-harm": result.categories.self_harm,
            "self-harm/intent": result.categories.self_harm_intent,
            "self-harm/instructions": result.categories.self_harm_instructions,
            "sexual": result.categories.sexual,
            "sexual/minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence/graphic": result.categories.violence_graphic,
        },
        "category_scores": {
            "hate": result.category_scores.hate,
            "hate/threatening": result.category_scores.hate_threatening,
            "harassment": result.category_scores.harassment,
            "harassment/threatening": result.category_scores.harassment_threatening,
            "self-harm": result.category_scores.self_harm,
            "self-harm/intent": result.category_scores.self_harm_intent,
            "self-harm/instructions": result.category_scores.self_harm_instructions,
            "sexual": result.category_scores.sexual,
            "sexual/minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence/graphic": result.category_scores.violence_graphic,
        },
    }
