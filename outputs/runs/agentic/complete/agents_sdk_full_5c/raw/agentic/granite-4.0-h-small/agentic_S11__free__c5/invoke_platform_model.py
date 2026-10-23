import os
from model_client import ManagedModelClient
from model_models import InvocationRequest, InvocationResponse

def invoke_platform_model(prompt: str) -> InvocationResponse:
    # Load client configuration from environment or config file
    client = ManagedModelClient()
    # Build request payload
    request = InvocationRequest(model="gpt-4o-mini", deployment="default", prompt=prompt)
    # Call the provider's hosted model API
    response = client.invoke(request)
    return response

if __name__ == "__main__":
    user_input = "Hello, how are you?"
    result = invoke_platform_model(user_input)
    print(result)