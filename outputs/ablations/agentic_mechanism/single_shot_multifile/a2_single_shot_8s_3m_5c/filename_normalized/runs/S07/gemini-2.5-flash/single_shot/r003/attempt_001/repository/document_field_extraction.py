import os
import json
from typing import Dict, Any

from anthropic import Anthropic, tool

from document_client import get_anthropic_client
from document_models import FieldExtractionInput, FieldExtractionOutput

def extract_structured_fields(
    field_extraction_input: FieldExtractionInput,
    model_name: str = "claude-3-5-sonnet-20240620", # Or other Anthropic model supporting tools
) -> FieldExtractionOutput:
    """Extracts structured fields from OCR-normalized document text using Anthropic Claude with tool use."""
    client = get_anthropic_client()

    # Dynamically create a tool schema based on the requested fields
    properties = {name: {"type": prop_type} for name, prop_type in field_extraction_input.fields_to_extract.items()}
    tool_schema = {
        "name": "extract_fields",
        "description": "Extracts specified structured fields from the input text.",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": list(field_extraction_input.fields_to_extract.keys()), # Assuming all requested fields are required
        },
    }

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Extract the following fields from the document text: {json.dumps(field_extraction_input.fields_to_extract)}. Document text: {field_extraction_input.document_text}"}
            ],
        }
    ]

    response = client.messages.create(
        model=model_name,
        max_tokens=2000,
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "extract_fields"},
        messages=messages,
    )

    extracted_fields: Dict[str, Any] = {}

    for content_block in response.content:
        if content_block.type == "tool_use" and content_block.name == "extract_fields":
            extracted_fields = content_block.input
            break

    return FieldExtractionOutput(extracted_fields=extracted_fields)
