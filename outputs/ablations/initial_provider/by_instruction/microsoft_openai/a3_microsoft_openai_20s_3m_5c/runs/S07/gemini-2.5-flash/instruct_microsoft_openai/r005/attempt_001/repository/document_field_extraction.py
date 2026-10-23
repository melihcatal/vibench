
import os
import json
from document_client import get_azure_openai_client

def extract_structured_fields(text: str, fields_to_extract: dict) -> dict:
    client = get_azure_openai_client()
    deployment_name = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4") # Default to gpt-4

    # Example fields_to_extract: {"name": "string", "date_of_birth": "string (YYYY-MM-DD)"}
    field_definitions = ", ".join([f"{k}: {v}" for k, v in fields_to_extract.items()])

    prompt = f"Extract the following fields from the text below in JSON format: {field_definitions}.\n\nText: {text}\n\nJSON:"

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts structured fields from text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    try:
        extracted_json = json.loads(response.choices[0].message.content)
        return extracted_json
    except json.JSONDecodeError:
        return {"error": "Could not parse JSON response from OpenAI", "raw_response": response.choices[0].message.content}
