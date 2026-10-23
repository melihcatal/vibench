import os
from google.cloud import aiplatform
from google.cloud.aiplatform.generative_models import GenerativeModel

def collect_platform_metadata(project_id: str, location: str, prompt: str):
    """
    Returns model output together with provider platform metadata such as usage.
    """
    aiplatform.init(project=project_id, location=location)

    model = GenerativeModel("gemini-pro")
    
    response = model.generate_content(prompt)

    # Extract model output
    model_output = response.text

    # Extract platform metadata
    # The 'usage_metadata' attribute contains information like total_token_count, prompt_token_count, etc.
    platform_metadata = {
        "candidate_count": len(response.candidates),
        "usage_metadata": response.usage_metadata.to_dict() if response.usage_metadata else {},
        "model_name": "gemini-pro", # Explicitly identify the model
        "provider": "google_cloud_aiplatform" # Explicitly identify the provider
    }

    return model_output, platform_metadata

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired location
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id") 
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    TEST_PROMPT = "What is the capital of France?"

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        print(f"Collecting platform metadata using Google Cloud Project ID: {PROJECT_ID}, Location: {LOCATION}")
        output, metadata = collect_platform_metadata(PROJECT_ID, LOCATION, TEST_PROMPT)
        print("\nModel Output:")
        print(output)
        print("\nPlatform Metadata:")
        print(metadata)
