from model_client import get_openai_client
import json

def extract_json(text: str, schema: dict) -> dict:
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert at extracting structured JSON data from text according to the following JSON schema: {json.dumps(schema)}. Only return the JSON object, no other text."},
            {"role": "user", "content": f"Extract JSON from the following text: {text}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)