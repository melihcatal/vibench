import vertexai
from vertexai.generative_models import GenerativeModel
import os


def collect_platform_metadata(
    project_id: str, location: str, model_name: str, prompt: str
):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    # Vertex AI responses contain various metadata. We'll extract some common ones.
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        "prompt_tokens": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
        "candidates_tokens": response.usage_metadata.candidates_token_count
        if response.usage_metadata
        else None,
        "total_tokens": response.usage_metadata.total_token_count
        if response.usage_metadata
        else None,
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
    }
    return response.text, metadata


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")
    test_prompt = "Tell me about large language models."
    if project_id:
        print(f"Invoking Vertex AI model {model_name} and collecting metadata...")
        output, metadata = collect_platform_metadata(
            project_id, location, model_name, test_prompt
        )
        print(f"Model Output: {output}")
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
