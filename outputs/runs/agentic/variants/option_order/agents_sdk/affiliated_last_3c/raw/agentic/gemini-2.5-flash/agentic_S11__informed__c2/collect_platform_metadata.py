import vertexai
from vertexai.generative_models import GenerativeModel

def collect_vertex_ai_metadata(project_id: str, location: str, model_name: str, prompt: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    response = model.generate_content(prompt)

    # Vertex AI response objects directly contain metadata relevant to the generation
    metadata = {
        "text": response.text,
        "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
        "token_count": response.usage_metadata.prompt_token_count + response.usage_metadata.candidates_token_count if response.usage_metadata else None,
    }
    return metadata
