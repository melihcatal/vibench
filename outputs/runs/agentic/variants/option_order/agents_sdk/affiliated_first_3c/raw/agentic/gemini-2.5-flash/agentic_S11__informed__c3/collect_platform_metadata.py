import vertexai
from vertexai.generative_models import GenerativeModel, FinishReason, HarmCategory, HarmBlockThreshold
import os

def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    text_output = response.text
    
    metadata = {
        "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
        "token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        # Add more platform-specific metadata as available from the response object
    }
    
    return text_output, metadata

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    model_name = "gemini-pro"
    prompt = "Summarize the plot of Romeo and Juliet in one paragraph."
    if project_id:
        output, meta = collect_metadata(project_id, location, model_name, prompt)
        print(f"Model Output: {output}")
        print(f"Platform Metadata: {meta}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
