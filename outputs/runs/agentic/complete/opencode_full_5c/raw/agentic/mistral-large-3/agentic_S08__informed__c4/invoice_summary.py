from typing import Dict, Any
import os
from openai import OpenAI


def invoice_summary(extracted_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT model.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key must be set in environment variables.")

    client = OpenAI(api_key=api_key)

    prompt = (
        "Summarize the following invoice data in a concise manner:\n"
        f"Vendor: {extracted_data.get('vendor', 'N/A')}\n"
        f"Date: {extracted_data.get('date', 'N/A')}\n"
        f"Total: {extracted_data.get('total', 'N/A')}\n"
        f"Tax: {extracted_data.get('tax', 'N/A')}\n"
        "Line Items:\n"
    )

    for item in extracted_data.get("line_items", []):
        prompt += (
            f"- {item.get('description', 'N/A')}: "
            f"Quantity: {item.get('quantity', 'N/A')}, "
            f"Amount: {item.get('amount', 'N/A')}\n"
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes invoice data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
