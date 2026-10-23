import os
import google.cloud.aiplatform as aiplatform

def stream_llm_completion(project_id: str, location: str, model_name: str = "gemini-pro"):
    """
    Streams partial output tokens from a hosted LLM using Google Cloud Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_name: The name of the model to use (default: "gemini-pro").
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name)

    # Example prompt
    prompt = "Tell me a short story about a brave knight."

    print(f"Streaming completion from model: {model_name}")
    print(f"Prompt: {prompt}\n")

    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        print(chunk.text, end="")
    print()

if __name__ == "__main__":
    # Replace with your actual Google Cloud project ID and location
    # You can also set these as environment variables
    # export GOOGLE_CLOUD_PROJECT="your-project-id"
    # export GOOGLE_CLOUD_LOCATION="your-location"
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if project_id == "your-gcp-project-id" or location == "your-location":
        print("Please set the GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables or update the script.")
    else:
        stream_llm_completion(project_id, location)
