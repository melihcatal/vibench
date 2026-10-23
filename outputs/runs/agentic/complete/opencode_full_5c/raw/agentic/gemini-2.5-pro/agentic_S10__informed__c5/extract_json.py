from model_client import get_gemini_client
import json


def extract_json_from_text_gemini(text_content: str) -> dict:
    """
    Extracts a JSON object from text using Gemini API with JSON mode.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Extract the user information from the following text and return it as a JSON object.
    The user's name is John Doe, he is 30 years old, and his email is john.doe@example.com.
    
    Text: '{text_content}'
    
    Return only the JSON object.
    """

    response = model.generate_content(
        prompt, generation_config={"response_mime_type": "application/json"}
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON from model response."}
