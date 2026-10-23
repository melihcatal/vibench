import json
from model_client import get_model_client

def extract_json_from_text(text_to_process: str) -> dict:
    """
    Extracts a structured JSON object from unstructured text.
    
    Args:
        text_to_process: The text containing information to be extracted.

    Returns:
        A dictionary with the extracted data.
    """
    client = get_model_client()
    
    prompt = f"""
    Extract the user's name, email, and company from the following text.
    Return the information as a valid JSON object with keys "name", "email", and "company".

    Text:
    "{text_to_process}"
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from text and returns it in JSON format."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        extracted_data = json.loads(response.choices[0].message.content)
        return extracted_data
    except (json.JSONDecodeError, IndexError):
        return {}

