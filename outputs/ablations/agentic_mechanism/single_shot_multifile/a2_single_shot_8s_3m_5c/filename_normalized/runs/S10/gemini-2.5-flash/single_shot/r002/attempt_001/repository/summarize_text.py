import os
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_gemini_model

def summarize_text(text: str) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    model = get_gemini_model(project_id, location, "gemini-pro")
    
    prompt = f"Summarize the following text:

{text}"
    
    response = model.generate_content(
        contents=prompt,
        generation_config={
            "max_output_tokens": 500,
            "temperature": 0.5,
            "top_p": 0.95,
        }
    )
    
    return response.text
