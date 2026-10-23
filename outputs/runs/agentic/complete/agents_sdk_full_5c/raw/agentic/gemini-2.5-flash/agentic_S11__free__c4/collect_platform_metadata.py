import vertexai
from vertexai.preview.language_models import TextGenerationModel
from typing import Dict, Any

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str) -> Dict[str, Any]:
    """Returns Google Cloud Vertex AI model output together with platform metadata."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_id)
    response = model.predict(prompt=prompt)
    
    metadata = {
        "text": response.text,
        "_raw_response_object": response, # Keep the raw object for full introspection if needed
        "citation_metadata": response.citation_metadata.citations if response.citation_metadata else []
        # Other potential metadata could be response.safety_attributes if available
    }
    return metadata
