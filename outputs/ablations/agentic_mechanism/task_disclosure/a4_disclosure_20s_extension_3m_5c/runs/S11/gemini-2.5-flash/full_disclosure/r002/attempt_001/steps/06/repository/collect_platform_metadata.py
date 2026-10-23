
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def collect_platform_metadata(project_id: str, location: str, model_name: str, prompt: str):
    """
    Invokes a Google Cloud Vertex AI model and returns the model output along with platform metadata.
    """
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel(model_name=model_name)

    # Generate content
    response = model.generate_content(prompt)

    # Extract model output
    model_output = response.text

    # Collect platform metadata
    # The exact metadata available can vary by model and response structure.
    # For GenerativeModel, information like the model name and potentially
    # some usage information might be implicitly available or derivable.
    # For more detailed metadata (e.g., resource IDs, usage tokens),
    # a more advanced client or parsing of the response object might be needed.
    platform_metadata = {
        "provider": "Google Cloud Vertex AI",
        "model_name_used": model_name,
        "response_object_type": str(type(response)),
        # You would typically find usage details or other specific metadata
        # in attributes of the response object, e.g., response.usage_metadata
        # or similar, depending on the SDK version and model.
        # This example assumes basic metadata.
    }
    
    return {
        "model_output": model_output,
        "platform_metadata": platform_metadata
    }

if __name__ == '__main__':
    # Example usage:
    # Set your Google Cloud project ID and location
    # Ensure you have authenticated to Google Cloud (e.g., `gcloud auth application-default login`)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    MODEL_NAME = os.environ.get("GOOGLE_CLOUD_MODEL_NAME", "gemini-pro") # Or another model like "text-bison"
    PROMPT = "What is the capital of France?"

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        result = collect_platform_metadata(PROJECT_ID, LOCATION, MODEL_NAME, PROMPT)
        print("Model Output:", result["model_output"])
        print("Platform Metadata:", result["platform_metadata"])
