from document_client import get_openai_client
import os
import json
from document_client import get_openai_client

def extract_structured_fields(text: str, schema: dict) -> dict:
    client = get_openai_client()
    
    # Convert the schema dictionary to a JSON string for the prompt
    schema_str = json.dumps(schema, indent=2)

    system_message = (
        "You are an AI assistant designed to extract structured information from text according to a provided JSON schema.\n"
        "Your response MUST be a JSON object that strictly adheres to the provided schema. "
        "If a field cannot be found, omit it or set its value to null based on schema requirements (e.g., if nullable).\n"
        "Only return the JSON object, do not include any other text or explanations."
    )

    user_message = (
        f"Extract information from the following text based on the JSON schema provided:\n\n"
        f"Text:\n{text}\n\n"
        f"Schema:\n{schema_str}\n\n"
        "Please return only the JSON object." 
    )

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-35-turbo"), # Use deployment name
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        response_format={ "type": "json_object" }
    )
    
    extracted_json_str = response.choices[0].message.content
    return json.loads(extracted_json_str)

