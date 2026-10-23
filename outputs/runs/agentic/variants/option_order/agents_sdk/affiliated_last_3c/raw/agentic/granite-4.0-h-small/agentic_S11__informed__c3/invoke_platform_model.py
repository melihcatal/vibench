import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest

def invoke_platform_model(deployment_id: str, prompt: str) -> dict:
    # Load client from environment or config
    client = ManagedModelClient.from_env()
    # Build a request object using local helpers
    request = ModelInvocationRequest(
        deployment=deployment_id,
        prompt=prompt
    )
    # Invoke the provider-managed model through the client
    response = client.invoke(request)
    return response.dict()  # Return serialized response

# Example usage (guarded by __main__ to avoid execution when imported)
if __name__ == "__main__":
    # Assume deployment ID is set in env variable DEPLOYMENT_ID
    deployment_id = os.getenv("DEPLOYMENT_ID")
    if not deployment_id:
        raise RuntimeError("DEPLOYMENT_ID environment variable must be set")
    user_prompt = "How are you?"
    result = invoke_platform_model(deployment_id, user_prompt)
    print(result)
