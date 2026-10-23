import os
import anthropic
from document_models import NormalizedExpense


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def summarize_invoice_fields(normalized_expense: NormalizedExpense) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    expense_data = normalized_expense.to_dict()
    line_items_text = ""
    if expense_data.get("line_items"):
        for idx, item in enumerate(expense_data["line_items"], 1):
            if isinstance(item, dict):
                desc = item.get("description", "N/A")
                amount = item.get("amount", item.get("price", "N/A"))
                line_items_text += f"  {idx}. {desc} - ${amount}\n"
            else:
                line_items_text += f"  {idx}. {item}\n"

    prompt = (
        f"Summarize the following invoice data in 2-3 sentences:\n"
        f"Document Type: {expense_data.get('document_type', 'N/A')}\n"
        f"Vendor/Merchant: {expense_data.get('vendor_or_merchant', 'N/A')}\n"
        f"Date: {expense_data.get('date', 'N/A')}\n"
        f"Subtotal: ${expense_data.get('subtotal', 'N/A')}\n"
        f"Tax: ${expense_data.get('tax', 'N/A')}\n"
        f"Total: ${expense_data.get('total', 'N/A')}\n"
        f"Currency: {expense_data.get('currency', 'USD')}\n"
        f"Line Items:\n{line_items_text if line_items_text else '  None listed'}\n"
        f"Confidence Score: {expense_data.get('confidence', 'N/A')}"
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )

    summary = ""
    if message.content:
        for block in message.content:
            if hasattr(block, "text"):
                summary += block.text
    return summary.strip()


def summarize_invoice_from_dict(expense_dict: dict) -> str:
    normalized = NormalizedExpense(
        document_type=expense_dict.get("document_type", ""),
        vendor_or_merchant=expense_dict.get("vendor_or_merchant", ""),
        date=expense_dict.get("date", ""),
        subtotal=expense_dict.get("subtotal", 0.0),
        tax=expense_dict.get("tax", 0.0),
        total=expense_dict.get("total", 0.0),
        line_items=expense_dict.get("line_items", []),
        currency=expense_dict.get("currency", "USD"),
        confidence=expense_dict.get("confidence", 0.0),
    )
    return summarize_invoice_fields(normalized)
