# [LATER-STEP] invoice_summary.py

# Summarizes extracted invoice fields using DashScope Qwen

import os
from dashscope import ChatCompletion

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
assert DASHSCOPE_API_KEY, "Set DASHSCOPE_API_KEY"


def summarize_invoice(extracted: Dict[str, Any]) -> str:
    """Generate a concise summary of an invoice using Qwen (DashScope)."""
    prompt = f"Summarize this invoice in two sentences:\nVendor: {extracted.get('vendor', 'N/A')}\nDate: {extracted.get('invoice_date', 'N/A')}\nTotal: {extracted.get('total_amount', 'N/A')}\nItems:\n{', '.join(item.get('description', '') for item in extracted.get('line_items', []))}"
    client = ChatCompletion()
    response = client.chat(model="qwen", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
