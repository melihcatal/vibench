import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def collect_platform_metadata(prompt: str, project_id: str, location: str, model_name: str = "gemini-pro") -> dict:
    """Returns model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    output = {
        "text": response.text,
        "metadata": {
            "model_name": model_name,
            "project_id": project_id,
            "location": location,
            "usage_metadata": response.usage_metadata.to_dict() if response.usage_metadata else {},
            "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN"
        }
    }
    return output

if __name__ == '__main__':
    # Example usage (replace with your actual project_id and location)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project_id:
        result_with_metadata = collect_platform_metadata("List three interesting facts about the ocean.", project_id, location)
        print("Model output with metadata:")
        print(f"Text: {result_with_metadata['text']}")
        print(f"Metadata: {result_with_metadata['metadata']}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
