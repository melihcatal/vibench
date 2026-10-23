from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
from typing import Dict, Any

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str) -> Dict[str, Any]:
    """
    Invokes a Google Cloud Vertex AI model and collects platform metadata.
    """
    aiplatform.init(project=project_id, location=location)
    
    text_model = TextGenerationModel.from_pretrained(model_id)
    response = text_model.predict(prompt=prompt)
    
    metadata = {
        "model_output": response.text,
        "model_id": model_id,
        "platform": "Google Cloud Vertex AI",
        "citation_metadata": response.citation_metadata.citations[0].url if response.citation_metadata and response.citation_metadata.citations else None
        # In a real scenario, more detailed metadata like token usage, safety attributes etc. would be extracted if available
    }
    
    return metadata
