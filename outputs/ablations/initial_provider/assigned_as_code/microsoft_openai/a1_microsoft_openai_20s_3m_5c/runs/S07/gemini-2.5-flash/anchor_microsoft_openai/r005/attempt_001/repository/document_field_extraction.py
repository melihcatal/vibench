
import os
import json
from openai import OpenAI
from document_client import get_openai_client
from document_models import DocumentField

def document_field_extraction(payload, config=None):
    config = config or {}
    
    openai_api_key = os.environ.get("OPENAI_API_KEY") or config.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable/config.")
    
    client = get_openai_client(openai_api_key)

    # The fields to extract should be provided in the config or payload
    # For this example, let's assume a generic extraction of 'name' and 'address'
    # In a real scenario, the prompt would be dynamically generated based on required fields.
    fields_to_extract = config.get("FIELDS_TO_EXTRACT", ["name", "address", "invoice_total"])

    prompt_messages = [
        {
            "role": "system", 
            "content": "You are an expert at extracting structured information from text. Extract the following fields from the provided document text as a JSON object: " + ", ".join(fields_to_extract) + ". If a field is not found, use an empty string. Output only the JSON object."
        },
        {
            "role": "user", 
            "content": f"Document Text: {payload['text']}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Using gpt-4o-mini as a cost-effective alternative for demonstration
        messages=prompt_messages,
        response_format={ "type": "json_object" }
    )

    extracted_data = json.loads(response.choices[0].message.content)

    document_fields = []
    for field_name, field_value in extracted_data.items():
        document_fields.append(DocumentField(field_name=field_name, field_value=str(field_value)))

    return document_fields
