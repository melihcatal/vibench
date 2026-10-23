import openai
from safety_client import get_openai_client
from safety_models import ModerationResponse, ModerationRequest

def moderate_text(text: str) -> ModerationResponse:
    client = get_openai_client()
    response = client.moderations.create(input=text)
    
    # Normalize the OpenAI response to our internal ModerationResponse model
    # This is a simplified example; actual normalization might be more complex
    result = response.results[0]
    category_scores = {
        k: getattr(result.category_scores, k) for k in result.category_scores.__dict__.keys()
    }
    categories = {
        k: getattr(result.categories, k) for k in result.categories.__dict__.keys()
    }

    return ModerationResponse(
        id=response.id,
        model=response.model,
        categories=categories,
        category_scores=category_scores,
        flagged=result.flagged
    )
