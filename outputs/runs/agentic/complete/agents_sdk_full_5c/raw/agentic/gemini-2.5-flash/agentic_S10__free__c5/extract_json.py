from vertexai.preview.language_models import TextGenerationModel

from model_client import get_palm_model

def extract_json(text: str) -> str:
    model = get_palm_model()
    prompt = f"""Extract a JSON object containing 'name' and 'age' from the following text:
{text}
JSON:"""
    response = model.predict(
        prompt,
        temperature=0.1,
        max_output_tokens=512,
    )
    return response.text
