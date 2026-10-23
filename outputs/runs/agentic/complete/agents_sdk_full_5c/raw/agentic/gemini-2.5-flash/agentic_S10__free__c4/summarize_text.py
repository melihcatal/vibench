import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os

def summarize_text(text: str) -> str:
    """Summarizes the given text using a hosted LLM."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")
    
    prompt = f"Summarize the following text:

{text}\n\nSummary:"
    
    response = model.predict(
        prompt,
        max_output_tokens=256,
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )
    return response.text
