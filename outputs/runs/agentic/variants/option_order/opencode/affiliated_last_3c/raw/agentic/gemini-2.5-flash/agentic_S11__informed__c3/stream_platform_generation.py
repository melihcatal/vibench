import vertexai
from vertexai.generative_models import GenerativeModel
import os


def stream_platform_generation(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        yield response.text


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")
    test_prompt = "Tell me a long story about a magical cat."
    if project_id:
        print(f"Streaming from Vertex AI model {model_name}...")
        for chunk in stream_platform_generation(
            project_id, location, model_name, test_prompt
        ):
            print(chunk, end="")
        print("\nStream complete.")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
