import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest

def invoke_platform_model(deployment_id: str, prompt: str) -> dict:
    """Invoke a managed model using a provider-specific deployment ID.
    Args:
        deployment_id: Identifier of the model deployment on the platform.
        prompt: Input text for the model.
    Returns:
        Dictionary containing model response and provider metadata.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(deployment_id=deployment_id, prompt=prompt)
    response = client.invoke(request)
    return response.serialize()

if __name__ == "__main__":
    # Example usage with Azure OpenAI deployment
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_ID = "gpt-4o-mini"  # Azure OpenAI model deployment name
    prompt = "What is the capital of France?"
    result = invoke_platform_model(DEPLOYMENT_ID, prompt)
    print(result)