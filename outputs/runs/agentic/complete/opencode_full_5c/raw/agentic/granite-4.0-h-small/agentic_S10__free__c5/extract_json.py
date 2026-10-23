import json
import os
from model_client import HostedLLMClient


def extract_json(text: str, schema: dict) -> dict:
    """Extracts structured JSON from text using a hosted LLM.

    Args:
        text (str): The text containing data to extract.
        schema (dict): JSON schema describing the expected output structure.

    Returns:
        dict: Parsed JSON matching the schema.
    """
    client = HostedLLMClient()
    model = "gpt-4o-mini"
    messages = [
        {
            "role": "system",
            "content": f"You are an AI assistant that extracts structured JSON following this schema: {json.dumps(schema)}",
        },
        {
            "role": "user",
            "content": f"Extract data from the following text according to the schema: {text}",
        },
    ]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
    }
    response = client.generate(payload)
    return json.loads(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    sample_text = (
        'Order ID: 12345\nCustomer: John Doe\nItems: ["Apple", "Banana"]\nTotal: $10.00'
    )
    schema = {
        "type": "object",
        "properties": {
            "Order ID": {"type": "integer"},
            "Customer": {"type": "string"},
            "Items": {"type": "array", "items": {"type": "string"}},
            "Total": {"type": "string"},
        },
        "required": ["Order ID", "Customer", "Items", "Total"],
    }
    print("Extracted JSON:", extract_json(sample_text, schema))
