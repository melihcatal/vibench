from vertexai.preview.language_models import TextGenerationModel
import os

def stored_asset_summary(payload):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # e.g., 'us-central1'
    
    if not all([project_id, location]):
        raise ValueError("Google Cloud Project ID or Location not found in environment variables.")

    text_content = payload['text_content']
    min_length = payload.get('min_length', 50)
    max_length = payload.get('max_length', 200)

    # Initialize Vertex AI
    # Note: Vertex AI models are regional, so ensure the client is configured for the correct location.
    # For preview models like TextGenerationModel, the region might be specific.
    # Using a common region like us-central1 for demonstration.
    
    model = TextGenerationModel.from_pretrained("gemini-pro") # Using gemini-pro for summarization
    
    prompt = f"Summarize the following text in {min_length} to {max_length} words:\n\n{text_content}"

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256, # Adjust based on desired summary length
    )

    return {'summary': response.text, 'original_text_length': len(text_content)}
