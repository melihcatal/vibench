# invoke_platform_model.py
# [SAME-SCENARIO]
# Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client

import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse


def invoke_model(
    project_id: str,
    deployment_id: str,
    model_input: str,
    profile: str = "default",
) -> ModelInvocationResponse:
    """Invoke the managed model and return a standardized response object."""
    # Build request payload
    request = ModelInvocationRequest(
        project_id=project_id,
        deployment_id=deployment_id,
        input_text=model_input,
        profile=profile,
    )
    # Use the concrete provider client (e.g., OpenAI)
    client = ManagedModelClient(provider="openai")
    raw_response = client.invoke(request)
    # Normalize response
    return ModelInvocationResponse.from_raw(raw_response)


# Example usage (uncomment to run locally)
# if __name__ == "__main__":
#     resp = invoke_model(
#         project_id="my-project",
#         deployment_id="my-deployment",
#         model_input="Hello, world!",
#     )
#     print(json.dumps(resp.to_dict(), indent=2))
