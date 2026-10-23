from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel

def stream_completion(project_id: str, location: str, prompt: str, model_name: str = "gemini-pro"):
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    
    responses = model.generate_content(prompt, stream=True)
    
    for response in responses:
        yield response.text
