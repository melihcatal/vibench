import os
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import Type


def document_field_extraction(
    document_text: str, pydantic_schema: Type[BaseModel]
) -> BaseModel:
    """
    Extracts structured fields from document text based on a Pydantic schema.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    schema_json = pydantic_schema.model_json_schema()

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_document_fields",
                "description": "Extracts the required fields from the document text.",
                "parameters": schema_json,
            },
        }
    ]

    prompt = f"Extract the relevant information from the following document text according to the provided schema:\n\n{document_text}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "extract_document_fields"},
        },
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        function_args = json.loads(tool_calls[0].function.arguments)
        return pydantic_schema(**function_args)
    else:
        raise ValueError("Failed to extract fields from the document.")
