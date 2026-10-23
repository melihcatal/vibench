import json
from openai import OpenAI
from document_client import get_openai_client
from document_models import NormalizedExpense
from typing import Dict, Any

def normalize_expense_llm(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema using OpenAI GPT-4o.
    Requires OPENAI_API_KEY environment variable.
    """
    client = get_openai_client()

    prompt_schema = NormalizedExpense.model_json_schema()
    prompt_schema_copy = prompt_schema.copy()
    if 'properties' in prompt_schema_copy and 'original_extracted_data' in prompt_schema_copy['properties']:
        del prompt_schema_copy['properties']['original_extracted_data']
    if 'required' in prompt_schema_copy and 'original_extracted_data' in prompt_schema_copy['required']:
        prompt_schema_copy['required'].remove('original_extracted_data')

    messages = [
        {
            "role": "system",
            "content": f"""You are an expert at normalizing expense data.
            Convert the provided raw extracted expense data into a standard JSON schema.
            The document type is '{document_type}'.
            The output must be a JSON object strictly adhering to this Pydantic schema:
            {json.dumps(prompt_schema_copy, indent=2)}
            Ensure the 'line_items' are converted into a list of generic dictionaries, preserving relevant details like description, quantity, amount.
            Infer a 'category' if possible (e.g., "Food", "Travel", "Office Supplies"). If not, use "Uncategorized".
            Convert dates to ISO 8601 format (YYYY-MM-DD) if possible.
            If a field is missing or cannot be inferred, omit it from the output JSON unless it's explicitly marked as required by the schema and you can provide a default.
            """
        },
        {
            "role": "user",
            "content": f"Raw extracted data (from {document_type}):\n{json.dumps(extracted_data, indent=2)}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages,
        temperature=0.0
    )

    normalized_data_json = response.choices[0].message.content
    normalized_dict = json.loads(normalized_data_json)

    normalized_dict['original_extracted_data'] = extracted_data
    normalized_dict['document_type'] = document_type

    return NormalizedExpense(**normalized_dict)
