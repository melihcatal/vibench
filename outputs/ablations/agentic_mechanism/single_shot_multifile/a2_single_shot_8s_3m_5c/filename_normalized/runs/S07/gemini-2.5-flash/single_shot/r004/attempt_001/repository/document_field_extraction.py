import os
import json
import anthropic
from document_client import get_anthropic_client
from document_models import FieldExtractionResult

def extract_structured_fields(text: str, schema: dict, model_name: str = "claude-3-opus-20240229") -> FieldExtractionResult:
    client = get_anthropic_client()

    tool_definition = {
        "name": "extract_document_fields",
        "description": "Extracts structured data fields from a document based on a predefined schema.",
        "input_schema": schema
    }

    message = client.messages.create(
        model=model_name,
        max_tokens=2048,
        tools=[tool_definition],
        messages=[
            {"role": "user", "content": f"Extract the following structured fields from the document text below:\n\n---\nDocument Text:\n{text}\n---\n\nIf a field is not found, omit it unless it is required by the schema."}
        ]
    )

    extracted_data = {}
    if message.stop_reason == "tool_use":
        for content_block in message.content:
            if content_block.type == "tool_use":
                if content_block.name == "extract_document_fields":
                    extracted_data = content_block.input
                    break
    
    return FieldExtractionResult(extracted_fields=extracted_data)