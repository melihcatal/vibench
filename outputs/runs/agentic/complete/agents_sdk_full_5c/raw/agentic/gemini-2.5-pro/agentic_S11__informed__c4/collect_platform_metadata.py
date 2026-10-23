from model_client import get_model_client, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
from model_models import ModelResponse

def invoke_with_metadata(prompt: str) -> ModelResponse:
    """
    Invokes a deployed model and returns its output along with platform metadata.
    
    Args:
        prompt: The user prompt to send to the model.

    Returns:
        A ModelResponse object containing the generated text and metadata.
    """
    client = get_model_client()
    deployment_name = AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    
    response = client.chat.completions.create(
        model=deployment_name, # e.g. "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
    )
    
    text_content = response.choices[0].message.content if response.choices else None

    # Extract relevant metadata from the Azure OpenAI response object
    metadata = {
        "model_id": response.model,
        "usage": {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "id": response.id,
        "created": response.created,
        "system_fingerprint": response.system_fingerprint,
    }
    
    return ModelResponse(text=text_content, metadata=metadata)
