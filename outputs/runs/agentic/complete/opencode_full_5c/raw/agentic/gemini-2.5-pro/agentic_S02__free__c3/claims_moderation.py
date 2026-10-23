import openai
import os
from identity_models import ModerationResult


def moderate_text_claim(text: str) -> ModerationResult:
    """
    Moderates a free-text claim using OpenAI's Moderation API.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.Moderation.create(input=text, model="text-moderation-latest")

    result = response["results"][0]

    return ModerationResult(flagged=result["flagged"], categories=result["categories"])


# Required environment variable:
# export OPENAI_API_KEY="your_openai_api_key"
