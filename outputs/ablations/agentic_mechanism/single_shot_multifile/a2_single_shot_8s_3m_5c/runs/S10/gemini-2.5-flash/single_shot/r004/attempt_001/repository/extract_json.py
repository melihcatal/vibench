from model_client import get_openai_client
from model_models import ChatMessage
import json

def extract_json(text: str, json_schema: dict, model_id: str = "gpt-4o") -> dict:
    client = get_openai_client()
    messages = [
        ChatMessage(role="system", content=f"You are an expert at extracting structured JSON data from text. Extract information according to this JSON schema: {json.dumps(json_schema)}"),
        ChatMessage(role="user", content=f"Extract the relevant information as a JSON object from the following text:
\n{text}")
    ]
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[m.to_dict() for m in messages],
            response_format={"type": "json_object"},
            max_tokens=500,
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return {}
