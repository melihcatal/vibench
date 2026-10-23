from model_models import ModelResponse, InvocationMetadata
from invoke_platform_model import invoke_model


def get_model_response_with_metadata(prompt: str) -> ModelResponse:
    """
    Returns model output together with provider platform metadata.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        A ModelResponse object with the generated text and usage metadata.
    """
    model_response = invoke_model(prompt)

    # The invoke_model function already populates the metadata.
    # This function demonstrates retrieving it.
    if model_response.raw_response and model_response.raw_response.usage_metadata:
        usage = model_response.raw_response.usage_metadata
        model_response.metadata = InvocationMetadata(
            prompt_token_count=usage.prompt_token_count,
            candidates_token_count=usage.candidates_token_count,
            total_token_count=usage.total_token_count,
        )
    return model_response


if __name__ == "__main__":
    try:
        sample_prompt = "Why is the sky blue?"
        response = get_model_response_with_metadata(sample_prompt)
        print(f"Response text: {response.text}")
        if response.metadata:
            print(f"Platform metadata: {response.metadata.model_dump_json(indent=2)}")
        else:
            print("No metadata was collected.")
    except (ValueError, ImportError) as e:
        print(f"Error collecting metadata: {e}")
