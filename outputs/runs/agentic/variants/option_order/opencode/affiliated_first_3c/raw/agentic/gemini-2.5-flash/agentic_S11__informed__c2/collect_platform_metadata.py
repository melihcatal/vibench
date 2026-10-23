import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image


def collect_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)
    metadata = {
        "text": response.text,
        "usage_metadata": response.usage_metadata,
        "candidates": [
            {
                "finish_reason": c.finish_reason.name,
                "safety_ratings": [
                    {"category": s.category.name, "probability": s.probability.name}
                    for s in c.safety_ratings
                ],
            }
            for c in response.candidates
        ],
    }
    return metadata
