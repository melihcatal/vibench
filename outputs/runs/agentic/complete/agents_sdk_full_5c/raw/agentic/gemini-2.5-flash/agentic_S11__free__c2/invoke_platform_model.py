import vertexai
from vertexai.language_models import TextGenerationModel

def invoke_platform_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a managed model platform with a given prompt."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt=prompt)
    return response.text
