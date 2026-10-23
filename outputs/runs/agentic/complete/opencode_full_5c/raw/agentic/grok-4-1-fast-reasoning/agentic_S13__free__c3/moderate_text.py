import openai
from safety_client import get_api_key
from safety_models import ModerationResult, normalize_categories


def moderate_text(text: str) -> ModerationResult:
    client = openai.OpenAI(api_key=get_api_key("openai"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    raw_scores = {k: result.category_scores[k] for k in result.category_scores}
    scores = normalize_categories(raw_scores)
    flagged = result.flagged
    return ModerationResult(input_text=text, scores=scores, flagged=flagged)
