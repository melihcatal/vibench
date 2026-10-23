from typing import Dict, Any, Optional
import json
from openai import OpenAI
import os


def summarize_invoice_fields(extracted_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        "Summarize the following invoice data in a concise and professional manner:\n"
        f"Vendor: {extracted_data.get('vendor', 'N/A')}\n"
        f"Date: {extracted_data.get('date', 'N/A')}\n"
        f"Total: {extracted_data.get('total', 'N/A')}\n"
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
                "content": "You are a professional assistant that summarizes invoice data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
