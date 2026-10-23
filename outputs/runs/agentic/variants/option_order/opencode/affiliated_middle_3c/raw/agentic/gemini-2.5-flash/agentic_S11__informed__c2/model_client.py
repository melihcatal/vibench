import vertexai
import os


def get_vertex_ai_model(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)
    return vertexai.preview.language_models.TextGenerationModel.from_pretrained(
        model_name
    )
