import os
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import prediction_service


def invoke_platform_model(prompt: str, deployment_name: str = "text-bison") -> str:
    """Invoke a provider-managed model through a deployment-scoped platform client."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": prompt}]
    parameters = {"temperature": 0.2, "maxOutputTokens": 256, "topP": 0.95, "topK": 40}

    response = endpoint.predict(instances=instances, parameters=parameters)

    if response.predictions and len(response.predictions) > 0:
        return response.predictions[0].get("content", "")
    return ""


if __name__ == "__main__":
    test_prompt = "Explain quantum computing in simple terms."
    result = invoke_platform_model(test_prompt, "text-bison-32k")
    print(f"Model response: {result[:100]}...")
