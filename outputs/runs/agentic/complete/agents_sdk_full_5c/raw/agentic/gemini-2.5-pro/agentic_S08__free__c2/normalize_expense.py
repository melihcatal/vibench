import os
import json
from typing import Dict, Any

from openai import OpenAI
from document_models import NormalizedExpense

def normalize_expense(
    extracted_data: Dict[str, Any],
    target_schema: Dict[str, Any]
) -> NormalizedExpense:
    """
    Normalizes extracted expense data to a standard schema using OpenAI.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    prompt = f"""
    Please normalize the following extracted document data into the provided JSON schema.
    The goal is to map the source fields to the target schema fields accurately.
    Ensure data types are correct (e.g., numbers for amounts, ISO format for dates).

    Extracted Data:
    {json.dumps(extracted_data, indent=2)}

    Target JSON Schema:
    {json.dumps(target_schema, indent=2)}

    Respond with ONLY the populated JSON object.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data normalization expert."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    normalized_data = json.loads(response.choices[0].message.content)
    return NormalizedExpense(**normalized_data)
