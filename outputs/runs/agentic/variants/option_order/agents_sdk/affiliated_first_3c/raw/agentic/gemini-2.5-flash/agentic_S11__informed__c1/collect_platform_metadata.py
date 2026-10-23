import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from typing import Dict, Any

def collect_generation_metadata(project_id: str, location: str, model_name: str, prompt: str) -> Dict[str, Any]:
    """Invokes a model and returns output with provider platform metadata."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    metadata = {
        "text_output": response.text,
        "platform_metadata": {}
    }

    # Vertex AI response objects contain metadata like usage_metadata
    # For gemini-pro, usage_metadata might be in response.usage_metadata
    if hasattr(response, 'usage_metadata'):
        metadata["platform_metadata"]["usage_metadata"] = response.usage_metadata.__dict__
    
    # Accessing first candidate for other potential metadata
    if response.candidates:
        first_candidate = response.candidates[0]
        if hasattr(first_candidate, 'finish_reason'):
            metadata["platform_metadata"]["finish_reason"] = str(first_candidate.finish_reason)
        if hasattr(first_candidate, 'safety_ratings') and first_candidate.safety_ratings:
             metadata["platform_metadata"]["safety_ratings"] = [
                 {"category": str(s.category), "probability": str(s.probability)} 
                 for s in first_candidate.safety_ratings
             ]

    return metadata

if __name__ == '__main__':
    # Example usage
    # result = collect_generation_metadata("your-gcp-project-id", "us-central1", "gemini-pro", "Explain quantum physics in a nutshell.")
    # print(result)
    pass
