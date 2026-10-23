import os
import openai
from identity_client import get_openai_api_key
from identity_models import ModerationRequest, ModerationResponse, ModerationResult

def profile_moderation(request: ModerationRequest) -> ModerationResponse:
    api_key = get_openai_api_key()
    client = openai.OpenAI(api_key=api_key)

    response = client.moderations.create(input=request["text"])
    
    results: list[ModerationResult] = []
    for res in response.results:
        results.append({
            "flagged": res.flagged,
            "categories": res.categories.model_dump(),
            "category_scores": res.category_scores.model_dump()
        })

    return {"results": results}