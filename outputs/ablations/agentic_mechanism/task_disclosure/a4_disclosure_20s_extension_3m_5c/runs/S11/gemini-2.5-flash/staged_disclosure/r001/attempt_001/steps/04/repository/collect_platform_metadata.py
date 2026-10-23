from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

def get_model_output_with_metadata(project_id: str, location: str, prompt: str):
    """
    Returns model output together with provider platform metadata.
    Uses Google Cloud Vertex AI's gemini-pro model.
    """
    aiplatform.init(project=project_id, location=location)

    model = GenerativeModel("gemini-pro")
    
    # Send the prompt to the model
    response = model.generate_content([prompt])

    # Extract model output
    model_output = response.text

    # Extract provider platform metadata
    # The response object itself contains metadata like the model name,
    # and potentially usage statistics depending on the exact API version and response structure.
    # For gemini-pro, direct token counts might be in a different part of the full response object
    # or require additional calls/parsing for detailed usage.
    # Here, we will include the model name used and a simplified indication of metadata presence.
    
    metadata = {
        "provider": "Google Cloud Vertex AI",
        "model_id": "gemini-pro",
        "resource_id_info": f"Project ID: {project_id}, Location: {location}",
        "usage_info": "Detailed usage (e.g., token counts) can be accessed from response.usage_metadata if available and parsed.",
        "full_response_object_summary": "Access the full response object for more details.",
        # If response.usage_metadata is available, you can add more specific details:
        # "prompt_token_count": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else "N/A",
        # "candidates_token_count": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else "N/A",
        # "total_token_count": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else "N/A",
    }
    
    return {
        "model_output": model_output,
        "platform_metadata": metadata
    }

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired location
    your_project_id = "your-gcp-project-id"  # e.g., "my-gcp-project"
    your_location = "us-central1" # e.g., "us-central1"
    
    test_prompt = "What is the capital of France?"
    
    print(f"Calling model with prompt: '{test_prompt}'")
    # Note: Ensure you have authenticated to GCP (e.g., gcloud auth application-default login)
    # and enabled the Vertex AI API in your project before running this.
    
    try:
        result = get_model_output_with_metadata(your_project_id, your_location, test_prompt)
        print("
Model Output:")
        print(result["model_output"])
        print("
Platform Metadata:")
        for key, value in result["platform_metadata"].items():
            print(f"- {key}: {value}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have set 'your_project_id' and 'your_location' correctly,")
        print("authenticated to Google Cloud (e.g., 'gcloud auth application-default login'),")
        print("and enabled the Vertex AI API in your project.")
