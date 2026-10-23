import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part


def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    """Returns model output and provider platform metadata from Google Cloud Vertex AI."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    metadata = {
        "text_output": response.text,
        "usage_metadata": getattr(
            response, "usage_metadata", None
        ),  # Access usage_metadata if available
        "model_id": model_name,
        "project_id": project_id,
        "location": location,
        "citation_metadata": getattr(response, "citation_metadata", None),
        "prompt_feedback": getattr(response, "prompt_feedback", None),
        "candidates": [
            {
                "finish_reason": candidate.finish_reason,
                "safety_ratings": [
                    {"category": s.category.name, "probability": s.probability.name}
                    for s in candidate.safety_ratings
                ],
            }
            for candidate in response.candidates
        ],
    }
    return metadata
