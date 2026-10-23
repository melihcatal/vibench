import json
from model_client import get_model_client
from model_models import ChatMessage

def extract_json(text_with_data: str) -> dict:
    """
    Extracts structured JSON from unstructured text using an OpenAI model.
    """
    client = get_model_client()
    
    prompt = f"""
    Extract the user's name, email, and age from the following text.
    Return the result as a JSON object with keys "name", "email", and "age".
    If a value is not found, use null.

    Text:
    "{text_with_data}"
    """
    
    messages = [
        ChatMessage(role="system", content="You are an expert at extracting structured data from text and providing it as a JSON object."),
        ChatMessage(role="user", content=prompt)
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[m.to_dict() for m in messages],
            response_format={"type": "json_object"},
        )
        
        extracted_data = response.choices[0].message.content
        return json.loads(extracted_data) if extracted_data else {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
