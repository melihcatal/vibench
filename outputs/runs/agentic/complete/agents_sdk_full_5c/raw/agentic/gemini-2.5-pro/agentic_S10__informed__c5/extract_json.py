import json
from model_client import generate_text
from model_models import ModelRequest, ModelResponse

def extract_json(unstructured_text: str) -> dict:
    """
    Calls a hosted LLM to extract structured JSON from text.
    """
    prompt = f"""
    Extract the name, company, and email address from the following text.
    Return the result as a valid JSON object with the keys "name", "company", and "email".

    Text:
    '''
    {unstructured_text}
    '''
    """
    
    request = ModelRequest(prompt=prompt, json_mode=True)
    response: ModelResponse = generate_text(request, model_name="gemini-1.5-flash")

    try:
        # The response text should be a JSON string
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_text)
    except (json.JSONDecodeError, AttributeError):
        # Handle cases where the model doesn't return perfect JSON
        return {"error": "Failed to parse JSON from model response", "raw_response": response.text}
