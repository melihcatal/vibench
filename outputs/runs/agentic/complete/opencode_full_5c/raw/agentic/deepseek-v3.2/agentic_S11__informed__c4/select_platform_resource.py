import os
from ibm_watsonx_ai import APIClient


def list_available_models():
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set"
        )

    client = APIClient(api_key=api_key, project_id=project_id)

    models = client.foundation_models.list()
    return models


def resolve_model_by_criteria(criteria):
    models = list_available_models()

    if "model_id" in criteria:
        for model in models:
            if model.get("model_id") == criteria["model_id"]:
                return model

    if "model_family" in criteria:
        matching_models = []
        for model in models:
            if criteria["model_family"].lower() in model.get("model_id", "").lower():
                matching_models.append(model)
        if matching_models:
            return matching_models[0]

    if "task_type" in criteria:
        task_type = criteria["task_type"].lower()
        task_mapping = {
            "chat": ["granite", "llama"],
            "code": ["granite-code", "starcoder"],
            "embedding": ["slate"],
            "instruction": ["granite", "mistral"],
        }

        for model in models:
            model_id = model.get("model_id", "").lower()
            for keyword in task_mapping.get(task_type, []):
                if keyword in model_id:
                    return model

    return None


def get_model_deployment(model_id):
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set"
        )

    client = APIClient(api_key=api_key, project_id=project_id)

    try:
        deployment = client.deployments.get(model_id)
        return deployment
    except:
        return None
