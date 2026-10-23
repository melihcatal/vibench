import os
import openai
import json
from typing import Dict, Any

from document_client import set_openai_api_key
from document_models import ExtractedFields

def extract_structured_fields(text: str, extraction_schema: Dict[str, Any]) -> ExtractedFields:
    set_openai_api_key()

    # The extraction_schema defines the desired output structure, often as a JSON schema.
    # For OpenAI's function calling, we provide it as a 'tool'.
    # For direct JSON mode, the prompt needs to clearly define the JSON structure.

    # Using JSON mode for direct structured output, assuming schema can be described in prompt
    # For more complex schemas, function calling would be more robust.
    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": f"You are an expert at extracting structured information from text. Extract the following fields as a JSON object: {json.dumps(extraction_schema)}. Ensure the output is valid JSON matching the specified structure and data types. If a field is not found, use null or an empty string/array as appropriate for its type."},
            {"role": "user", "content": f"Extract information from the following document text: {text}"}
        ]
    )

    extracted_data = json.loads(response.choices[0].message.content)

    return ExtractedFields(fields=extracted_data)
