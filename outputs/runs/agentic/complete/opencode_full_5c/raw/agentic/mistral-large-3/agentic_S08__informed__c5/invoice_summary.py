from typing import Dict, Any
import os
from openai import OpenAI


class InvoiceSummarizer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def summarize_invoice(self, invoice_data: Dict[str, Any]) -> str:
        prompt = (
            "Summarize the following invoice data in a concise manner:\n"
            f"Vendor: {invoice_data.get('vendor', 'N/A')}\n"
            f"Date: {invoice_data.get('date', 'N/A')}\n"
            f"Total: {invoice_data.get('total', 'N/A')}\n"
            "Line Items:\n"
        )
        for item in invoice_data.get("line_items", []):
            prompt += (
                f"- {item.get('description', 'N/A')}: {item.get('amount', 'N/A')}\n"
            )

        response = self.client.chat.completions.create(
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
