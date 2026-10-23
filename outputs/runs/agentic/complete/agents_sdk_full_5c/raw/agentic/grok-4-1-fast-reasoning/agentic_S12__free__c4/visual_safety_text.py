from openai import OpenAI
from vision_client import OPENAI_API_KEY
from vision_models import ModerationResult
from typing import List

def visual_safety_text(labels: List[str]) -> ModerationResult:
    client = OpenAI(api_key=OPENAI_API_KEY)
    text_to_check = ", ".join(labels)
    response = client.moderations.create(
        input=text_to_check,
        model="text-moderation-latest"
    )
    mod_result = response.results[0]
    flagged = mod_result.flagged
    categories = [cat for cat, val in mod_result.categories.items() if val] if flagged else None
    return ModerationResult(flagged=flagged, categories=categories)