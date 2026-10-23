from vertexai.preview.language_models import TextGenerationModel
import json

def extract_json(project_id: str, location: str, text_content: str) -> dict:
    """Extracts structured JSON from text using a Google Cloud Vertex AI PaLM model."""
    model = TextGenerationModel.from_pretrained("text-bison@002")
    prompt = f"""Extract the following information from the text below as a JSON object: name, email, phone. If a field is not found, use null.

Text: """{text_content}"""

JSON:
"""
    response = model.predict(
        prompt=prompt,
        temperature=0.0,
        max_output_tokens=512,
    )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from model output: {response.text}")
        return {}

