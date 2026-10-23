import os
from model_client import get_openai_client

def extract_json(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    
    prompt = (
        "Extract structured JSON from the following text. The JSON should conform to the schema: "
        "{\"name\": \"string\", \"age\": \"integer\", \"city\": \"string\"}. "
        "Return only the JSON object.\n\nText: " + payload['text']
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini', # Using a model known for better JSON capabilities
        messages=[{'role': 'user', 'content': prompt}],
        response_format={ "type": "json_object" }
    )
    return {'json_data': response.choices[0].message.content or ''}
