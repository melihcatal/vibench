import os
from model_client import get_vertex_ai_text_model
from model_models import ModelRequest, ModelResponse


def invoke_vertex_ai_model(
    project_id: str, location: str, prompt: str, model_name: str = "gemini-pro"
) -> ModelResponse:
    model = get_vertex_ai_text_model(
        project_id=project_id, location=location, model_name=model_name
    )
    response = model.generate_content(prompt)
    return ModelResponse(text=response.text)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    test_prompt = "What is the capital of France?"
    result = invoke_vertex_ai_model(
        project_id=project_id, location=location, prompt=test_prompt
    )
    print(f"Model Response: {result.text}")
