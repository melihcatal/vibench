import openai
from typing import List
from safety_client import get_openai_client
from safety_models import ModerationResponse

def moderate_batch(texts: List[str]) -> List[ModerationResponse]:
    client = get_openai_client()
    response = client.moderations.create(input=texts)
    
    batch_results = []
    for result in response.results:
        category_scores = {
            k: getattr(result.category_scores, k) for k in result.category_scores.__dict__.keys()
        }
        categories = {
            k: getattr(result.categories, k) for k in result.categories.__dict__.keys()
        }
        batch_results.append(ModerationResponse(
            id=response.id, # OpenAI returns one ID for the whole batch, might need adjustment for per-message ID if required
            model=response.model,
            categories=categories,
            category_scores=category_scores,
            flagged=result.flagged
        ))
    return batch_results
