from openai import OpenAI
from safety_client import safety_clients_config
from safety_models import ModerationInput, ModerationDecision, CategoryScores

def moderate_text(input_data: ModerationInput) -> ModerationDecision:
    """
    Scores user text for unsafe content using OpenAI's Moderation API.
    """
    client = OpenAI(api_key=safety_clients_config.OPENAI_API_KEY)

    response = client.moderations.create(
        input=input_data.text,
        model="text-moderation-stable"
    )

    result = response.results[0]

    # Map OpenAI response to our normalized model
    scores = result.category_scores
    decision = ModerationDecision(
        flagged=result.flagged,
        categories=result.categories.model_dump(),
        category_scores=CategoryScores(
            hate=scores.hate,
            hate_threatening=scores.hate_threatening,
            harassment=scores.harassment,
            harassment_threatening=scores.harassment_threatening,
            self_harm=scores.self_harm,
            self_harm_intent=scores.self_harm_intent,
            self_harm_instructions=scores.self_harm_instructions,
            sexual=scores.sexual,
            sexual_minors=scores.sexual_minors,
            violence=scores.violence,
            violence_graphic=scores.violence_graphic
        ),
        raw_response=response.model_dump()
    )

    return decision
