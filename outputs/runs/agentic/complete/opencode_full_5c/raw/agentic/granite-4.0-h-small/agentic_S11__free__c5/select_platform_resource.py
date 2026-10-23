# select_platform_resource.py
# [SAME-SCENARIO]
# Resolves a provider-specific model, deployment, or inference resource before invocation

import json
from model_client import ManagedModelClient
from model_models import ModelResourceRequest, ModelResourceResponse


def select_resource(
    project_id: str, model_name: str, resource_type: str = "model"
) -> ModelResourceResponse:
    """Select and return the concrete provider resource identifier."""
    request = ModelResourceRequest(
        project_id=project_id,
        name=model_name,
        type=resource_type,
    )
    client = ManagedModelClient(provider="openai")  # concrete provider
    raw_resp = client.resolve_resource(request)
    return ModelResourceResponse.from_raw(raw_resp)


# Example usage
# if __name__ == "__main__":
#     resp = select_resource(project_id="my-project", model_name="gpt-3.5-turbo", resource_type="model")
#     print(json.dumps(resp.to_dict(), indent=2))
