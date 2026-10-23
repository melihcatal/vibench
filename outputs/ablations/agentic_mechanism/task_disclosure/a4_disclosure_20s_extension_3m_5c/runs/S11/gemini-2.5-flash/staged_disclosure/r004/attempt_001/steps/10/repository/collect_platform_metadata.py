import os
from google.cloud import aiplatform

def collect_platform_metadata(prompt: str):
    """
    Returns model output together with provider platform metadata.
    Uses Google Cloud Vertex AI's GenerativeModel.
    """
    # Initialize Vertex AI
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))

    # Specify the model to use
    model_name = "gemini-pro"
    model = aiplatform.preview.generative_models.GenerativeModel(model_name)

    # Generate content
    response = model.generate_content(prompt)

    # Extract model output
    model_output = response.candidates[0].content.parts[0].text

    # Collect provider platform metadata
    metadata = {
        "provider": "Google Cloud Vertex AI",
        "model_name": model_name,
        # In a real-world scenario, you might find more detailed usage
        # or resource IDs in response objects depending on the SDK version and model.
        # For gemini-pro, token usage can be accessed via prompt_token_count and candidates_token_count.
        "usage": {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }
    }

    return {
        "model_output": model_output,
        "metadata": metadata
    }

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION are set as environment variables)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_CLOUD_REGION="us-central1" # Or your desired region
    test_prompt = "What is the capital of France?"
    result = collect_platform_metadata(test_prompt)
    print("Model Output:", result["model_output"])
    print("Metadata:", result["metadata"])
