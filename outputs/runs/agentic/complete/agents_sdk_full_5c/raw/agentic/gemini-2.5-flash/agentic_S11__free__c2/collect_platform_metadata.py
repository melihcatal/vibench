import vertexai
from vertexai.language_models import TextGenerationModel

def collect_platform_metadata(project_id: str, location: str, model_name: str, prompt: str):
    """Returns model output together with provider platform metadata."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt=prompt)

    metadata = {
        "text": response.text,
        "_raw_response_object": response, # For demonstration, preserving the full object
        "citation_metadata": response.citation_metadata.to_dict() if response.citation_metadata else None,
        "safety_attributes": response.safety_attributes.to_dict() if response.safety_attributes else None,
        # Vertex AI doesn't always expose token usage directly on the TextGenerationResponse
        # for predict, but for streaming or batch, it might be available.
        # This is a placeholder for where such metadata would typically be found.
        "usage_metadata": {"prompt_token_count": None, "candidates_token_count": None}
    }
    return metadata
