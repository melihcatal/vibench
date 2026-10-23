from google.cloud import aiplatform

def summarize_stored_asset_content(
    text_content: str,
    project_id: str,
    location: str = "us-central1"
) -> str:
    """Summarizes content extracted from a stored asset using Google Cloud Vertex AI (text-bison model)."""
    aiplatform.init(project=project_id, location=location)

    # Using the text-bison model for summarization
    # More information: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40
    }
    
    # Prepend a prompt for summarization
    prompt = f"Summarize the following text:\n\n{text_content}"

    model = aiplatform.TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(prompt, **parameters)

    return response.text
