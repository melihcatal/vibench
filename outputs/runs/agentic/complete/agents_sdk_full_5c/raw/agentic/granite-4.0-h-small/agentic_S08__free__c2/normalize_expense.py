# [SAME-SCENARIO] normalize_expense.py
"""
Normalize extracted expense fields into a standard JSON schema using OpenAI function calling.
"""
import json
import openai
from typing import TypedDict
from document_models import NormalizedExpense

class ExpenseInput(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: list[dict]

def normalize_expense(extracted: dict) -> NormalizedExpense:
    """Transform raw extraction results into normalized JSON schema.

    Args:
        extracted: Dict from upstream extractor with raw fields.

    Returns:
        NormalizedExpense adhering to a common contract.
    """
    # Example using OpenAI's function calling API for schema conversion
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data normalization engine. Convert the raw extraction JSON into the NormalizedExpense schema."},
            {"role": "user", "content": json.dumps(extracted)},
        ],
        functions=[
            {
                "name": "normalize",
                "parameters": "{\n  \"schema\": {\n    \"type\": \"object\",\n    \"properties\": {\n      \"vendor\": {\"type\": \"string\"},\n      \"date\": {\"type\": \"string\"},\n      \"total\": {\"type\": \"number\"},\n      \"line_items\": {\"type\": \"array\", \"items\": {\"type\": \"object\", \"properties\": {\"description\": {\"type\": \"string\"}, \"amount\": {\"type\": \"number\"}}}\n    }\n  }\n}"
            }
        ]
    )
    # Extract normalized payload from function response (placeholder parsing)
    normalized_json = response["function_calls"][0]["arguments"]
    return NormalizedExpense(**json.loads(normalized_json))
