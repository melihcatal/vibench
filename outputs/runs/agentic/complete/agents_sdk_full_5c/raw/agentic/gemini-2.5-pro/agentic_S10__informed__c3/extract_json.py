import json
from model_client import get_client

def extract_user_info(text: str) -> dict:
    """
    Extracts user information from text into a JSON object using an OpenAI model.
    """
    client = get_client()
    prompt = f"""
    Extract the user's name, email, and age from the following text.
    Return the information as a JSON object with keys "name", "email", and "age".
    If a piece of information is not present, use a null value.

    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data into JSON format."},
            {"role": "user", "content": prompt}
        ]
    )
    
    content = response.choices[0].message.content
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response"}
    return {}
