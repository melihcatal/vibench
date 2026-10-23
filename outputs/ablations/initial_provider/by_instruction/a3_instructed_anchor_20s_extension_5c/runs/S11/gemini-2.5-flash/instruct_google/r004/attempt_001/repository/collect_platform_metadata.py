from google.cloud import aiplatform

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str):
    """Returns model output together with Google Vertex AI platform metadata."""
    aiplatform.init(project=project_id, location=location)
    
    model = aiplatform.TextGenerationModel.from_pretrained(model_id)
    
    response = model.predict(prompt=prompt)
    
    # Vertex AI response objects contain metadata. For text generation, the response itself is often simple.
    # In more complex scenarios (e.g., batch predictions, custom models), more explicit metadata might be present.
    metadata = {
        "model_id": model_id,
        "text_length": len(response.text),
        "safety_attributes": response.safety_attributes.to_dict() if response.safety_attributes else None,
        # Add other relevant metadata if available in the response object
    }
    
    return {"text": response.text, "metadata": metadata}
