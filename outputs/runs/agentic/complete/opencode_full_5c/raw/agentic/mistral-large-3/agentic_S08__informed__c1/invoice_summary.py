from typing import Dict, Any
import os
from anthropic import Anthropic


class InvoiceSummarizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def summarize(self, normalized_data: Dict[str, Any]) -> str:
        prompt = (
            f"Summarize the following invoice details in a concise paragraph:\n\n"
            f"Vendor/Merchant: {normalized_data.get('vendor_or_merchant')}\n"
            f"Date: {normalized_data.get('date')}\n"
            f"Total Amount: {normalized_data.get('total_amount')} {normalized_data.get('currency')}\n"
            f"Items:\n"
        )
        for item in normalized_data.get("items", []):
            prompt += f"- {item.get('description')}: {item.get('quantity')} x {item.get('unit_price')} = {item.get('total_price')}\n"

        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
