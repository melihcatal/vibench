from vertexai.preview.generative_models import GenerativeModel
import vertexai

def collect_platform_metadata(project_id: str, location: str, model_name: str, prompt: str):
    """
    Returns model output together with Google Cloud Vertex AI platform metadata.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": 256},
        safety_settings={} # Placeholder to ensure settings can be passed
    )

    # Extract relevant metadata (this can vary based on the actual response structure)
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        "usage_metadata": { # Example of hypothetical usage metadata
            "prompt_token_count": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
            "candidates_token_count": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
            "total_token_count": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None,
        }
    }
    
    text_output = ""
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        text_output += part.text

    return {"text": text_output, "metadata": metadata}
