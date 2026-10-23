import os
import openai
from identity_models import ModerationRequest, ModerationResponse, ModerationResultCategory

openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

def moderate_profile_text(request: ModerationRequest) -> ModerationResponse:
    try:
        response = openai.moderations.create(input=request.text, model="text-moderation-latest")
        result = response.results[0]

        categories = ModerationResultCategory(
            harassment=result.categories.harassment,
            harassment_threatening=result.categories.harassment_threatening,
            hate=result.categories.hate,
            hate_threatening=result.categories.hate_threatening,
            self_harm=result.categories.self_harm,
            self_harm_intent=result.categories.self_harm_intent,
            self_harm_instructions=result.categories.self_harm_instructions,
            sexual=result.categories.sexual,
            sexual_minors=result.categories.sexual_minors,
            violence=result.categories.violence,
            violence_graphic=result.categories.violence_graphic
        )

        return ModerationResponse(
            id=response.id,
            flagged=result.flagged,
            categories=categories
        )
    except Exception as e:
        raise ValueError(f"OpenAI moderation failed: {e}")