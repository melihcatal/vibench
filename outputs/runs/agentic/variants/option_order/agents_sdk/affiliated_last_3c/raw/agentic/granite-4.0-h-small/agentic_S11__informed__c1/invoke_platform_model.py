import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_platform_model(resource_id: str, prompt: str) -> ModelInvocationResponse:
    """Invoke a managed model using the abstracted ManagedModelClient.
    Arguments:
        resource_id: Identifier for the model/deployment/inference profile.
        prompt: Input text for the model.
    Returns:
        A ModelInvocationResponse containing model output and metadata.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(resource_id=resource_id, prompt=prompt)
    response = client.invoke_model(request)
    return response

if __name__ == "__main__":
    # Example usage with environment variables for configuration
    RESOURCE_ID = os.getenv("MODEL_RESOURCE_ID")
    USER_PROMPT = os.getenv("USER_PROMPT", "Hello, model!")
    result = invoke_platform_model(RESOURCE_ID, USER_PROMPT)
    print(result)