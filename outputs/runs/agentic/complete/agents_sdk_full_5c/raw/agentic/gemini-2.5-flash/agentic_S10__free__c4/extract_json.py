import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os

def extract_json(text: str, schema: str) -> str:
    """Extracts structured JSON from text using a hosted LLM."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")
    
    prompt = f"""Extract information from the following text into a JSON object conforming to this schema:
Schema:
{schema}

Text:
{text}

JSON:
"""
    
    response = model.predict(
        prompt,
        max_output_tokens=1024,
        temperature=0.0, # Aim for deterministic output for JSON extraction
        top_p=0.8,
        top_k=40
    )
    return response.text
