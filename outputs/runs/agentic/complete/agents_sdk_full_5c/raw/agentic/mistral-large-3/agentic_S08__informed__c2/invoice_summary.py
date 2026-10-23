from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Dict, Any, Optional
import os

class InvoiceSummarizer:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-tiny"  # Concrete model identifier

    def summarize(self, normalized_data: Dict[str, Any]) -> Optional[str]:
        prompt = self._build_prompt(normalized_data)
        try:
            response = self.client.chat_completion(
                model=self.model,
                messages=[ChatMessage(role="user", content=prompt)]
            )
            return response.choices[0].message.content
        except Exception:
            return None

    def _build_prompt(self, normalized_data: Dict[str, Any]) -> str:
        vendor = normalized_data.get("vendor", "Unknown")
        total = normalized_data.get("total_amount", 0.0)
        date = normalized_data.get("date", "Unknown date")
        line_items = normalized_data.get("line_items", [])

        items_summary = "\n".join(
            [f"- {item.get('description', 'No description')} (Qty: {item.get('quantity', 1)}, Amount: {item.get('amount', 0.0)})"
             for item in line_items]
        )

        prompt = (
            f"Summarize the following invoice from {vendor} dated {date} with a total of ${total:.2f}. "
            f"Provide a concise summary of the key details and line items:\n\n"
            f"Line Items:\n{items_summary}\n\n"
            f"Summary:"
        )
        return prompt