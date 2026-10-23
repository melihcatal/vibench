import os
from openai import OpenAI
from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationResponse

def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    """
    Moderates a batch of user messages using OpenAI's moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    results: list[ModerationResponse] = []
    for msg_request in request.texts:
        response = client.moderations.create(input=msg_request.text)
        result = response.results[0]
        
        categories = {
            "harassment": result.categories.harassment,
            "harassment_threatening": result.categories.harassment_threatening,
            "hate": result.categories.hate,
            "hate_threatening": result.categories.hate_threatening,
            "self_harm": result.categories.self_harm,
            "self_harm_intent": result.categories.self_harm_intent,
            "self_harm_instruction": result.categories.self_harm_instruction,
            "sexual": result.categories.sexual,
            "sexual_minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence_graphic": result.categories.violence_graphic,
        }
        
        category_scores = {
            "harassment": result.category_scores.harassment,
            "harassment_threatening": result.category_scores.harassment_threatening,
            "hate": result.category_scores.hate,
            "hate_threatening": result.category_scores.hate_threatening,
            "self_harm": result.category_scores.self_harm,
            "self_harm_intent": result.category_scores.self_harm_intent,
            "self_harm_instruction": result.category_scores.self_harm_instruction,
            "sexual": result.category_scores.sexual,
            "sexual_minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence_graphic": result.category_scores.violence_graphic,
        }

        results.append(ModerationResponse(
            flagged=result.flagged,
            categories=categories,
            category_scores=category_scores
        ))
            
    return BatchModerationResponse(results=results)
