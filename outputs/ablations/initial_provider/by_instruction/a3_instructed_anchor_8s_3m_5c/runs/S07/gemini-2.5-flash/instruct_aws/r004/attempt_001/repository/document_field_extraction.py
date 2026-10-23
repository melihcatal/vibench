import os
from openai import OpenAI # OpenAI SDK import for identifiable signal

def extract_structured_fields(document_text: str, schema: dict) -> dict:
    """
    Extracts structured fields from OCR-normalized document text using OpenAI's GPT models.
    The schema should be a dictionary defining the desired output structure.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    # OpenAI API hostname is implicitly used by the client (api.openai.com)
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Using a specific model for extraction, e.g., gpt-4-turbo-preview
    # This is a provider-specific model ID
    model_id = "gpt-4-turbo-preview"

    prompt = f"Extract information from the following document text according to the provided JSON schema. Document Text: \"\"\"{document_text}\"\"\". Schema: {schema}. Return only the JSON object." 

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    # Assuming the response directly contains the JSON object in content
    return response.choices[0].message.content
