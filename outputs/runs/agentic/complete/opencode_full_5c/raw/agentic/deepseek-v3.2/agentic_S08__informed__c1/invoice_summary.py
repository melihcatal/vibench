import os
from typing import Dict, Any
from anthropic import Anthropic


def summarize_invoice_fields(invoice_data: Dict[str, Any]) -> str:
    """
    Summarize extracted invoice fields using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key not configured")

    client = Anthropic(api_key=api_key)

    vendor = invoice_data.get("vendor", "Unknown")
    date = invoice_data.get("date", "Unknown")
    total = invoice_data.get("total", 0.0)
    line_items = invoice_data.get("line_items", [])

    line_items_text = ""
    for i, item in enumerate(line_items, 1):
        desc = item.get("description", "No description")
        amount = item.get("amount", 0.0)
        quantity = item.get("quantity", 1.0)
        line_items_text += (
            f"{i}. {desc}: {quantity} × ${amount / quantity:.2f} = ${amount:.2f}\n"
        )

    prompt = f"""You are an expense analysis assistant. Summarize this invoice information:

Vendor: {vendor}
Date: {date}
Total Amount: ${total:.2f}

Line Items:
{line_items_text}

Please provide a concise summary that includes:
1. The main purpose of this invoice
2. Key items or services purchased
3. Any notable patterns or observations
4. A brief overall assessment

Keep the summary professional and under 150 words."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.content[0].text
        return summary.strip()

    except Exception as e:
        return f"Error generating summary: {str(e)}"
