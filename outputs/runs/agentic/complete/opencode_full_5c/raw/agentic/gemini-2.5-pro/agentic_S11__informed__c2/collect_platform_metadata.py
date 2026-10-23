from model_client import get_model
from model_models import InvokeRequest, InvokeResponse


def invoke_and_get_metadata(request: InvokeRequest) -> InvokeResponse:
    model = get_model()
    response = model.generate_content(request.prompt)

    usage_metadata = response.usage_metadata
    first_candidate = response.candidates[0]

    return InvokeResponse(
        text=first_candidate.content.parts[0].text,
        metadata={
            "prompt_token_count": usage_metadata.prompt_token_count,
            "candidates_token_count": usage_metadata.candidates_token_count,
            "total_token_count": usage_metadata.total_token_count,
            "finish_reason": first_candidate.finish_reason.name,
            "safety_ratings": [
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                }
                for rating in first_candidate.safety_ratings
            ],
        },
    )
