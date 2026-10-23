from model_models import ModelResponse, InvocationMetadata, InvocationSafetyRating
from select_platform_resource import select_model_resource
import vertexai.generative_models as gen_models


def invoke_model(prompt: str) -> ModelResponse:
    """
    Invokes a provider-managed model.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        A ModelResponse object containing the model's output and metadata.
    """
    model = select_model_resource()
    response = model.generate_content(prompt)

    first_candidate = response.candidates[0]

    text_response = first_candidate.content.parts[0].text

    metadata = InvocationMetadata(
        prompt_token_count=response.usage_metadata.prompt_token_count,
        candidates_token_count=response.usage_metadata.candidates_token_count,
        total_token_count=response.usage_metadata.total_token_count,
    )

    safety_ratings = [
        InvocationSafetyRating(
            category=rating.category.name,
            probability=rating.probability.name,
            blocked=rating.blocked,
        )
        for rating in first_candidate.safety_ratings
    ]

    return ModelResponse(
        text=text_response,
        metadata=metadata,
        safety_ratings=safety_ratings,
        raw_response=response,
    )


if __name__ == "__main__":
    try:
        sample_prompt = "What is the capital of France?"
        model_response = invoke_model(sample_prompt)
        print(f"Model response text: {model_response.text}")
        if model_response.metadata:
            print(
                f"Usage metadata: {model_response.metadata.model_dump_json(indent=2)}"
            )
    except (ValueError, ImportError) as e:
        print(f"Error invoking model: {e}")
