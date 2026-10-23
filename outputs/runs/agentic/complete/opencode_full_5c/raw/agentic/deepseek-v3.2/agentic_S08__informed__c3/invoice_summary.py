import os
import json
from typing import Dict, List, Any
from mistralai import Mistral
from document_models import InvoiceExtraction, NormalizedExpense


def summarize_invoice_fields(invoice: InvoiceExtraction) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=api_key)

    vendor = str(invoice.vendor_name.value) if invoice.vendor_name.value else "Unknown"
    date = (
        str(invoice.invoice_date.value)
        if invoice.invoice_date.value
        else "Unknown date"
    )
    total = float(invoice.invoice_total.value) if invoice.invoice_total.value else 0.0

    line_items_summary = []
    for i, item in enumerate(invoice.line_items[:5]):
        line_items_summary.append(
            f"{i + 1}. {item.description}: {item.quantity} x ${item.unit_price:.2f} = ${item.total_price:.2f}"
        )

    if len(invoice.line_items) > 5:
        line_items_summary.append(f"... and {len(invoice.line_items) - 5} more items")

    prompt = f"""Please provide a concise summary of this invoice:

Vendor: {vendor}
Invoice Date: {date}
Total Amount: ${total:.2f}

Line Items:
{chr(10).join(line_items_summary)}

Provide a 2-3 sentence summary highlighting the key details and any notable items."""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes invoice information concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.3,
    )

    return response.choices[0].message.content


def summarize_expense_record(expense: NormalizedExpense) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=api_key)

    line_items_summary = []
    for i, item in enumerate(expense.line_items[:3]):
        line_items_summary.append(
            f"{i + 1}. {item['description']}: ${item['total']:.2f}"
        )

    if len(expense.line_items) > 3:
        line_items_summary.append(f"... and {len(expense.line_items) - 3} more items")

    prompt = f"""Summarize this expense record:

Expense ID: {expense.expense_id}
Vendor: {expense.vendor}
Date: {expense.date.strftime("%Y-%m-%d")}
Total: {expense.currency} {expense.total_amount:.2f}
Confidence Score: {expense.confidence_score:.2%}

Top Items:
{chr(10).join(line_items_summary)}

Provide a brief 2-sentence summary suitable for expense reporting."""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You summarize expense records for financial reporting.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.2,
    )

    return response.choices[0].message.content


def generate_expense_category(expense: NormalizedExpense) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=api_key)

    item_descriptions = [item["description"] for item in expense.line_items[:5]]
    items_text = ", ".join(item_descriptions)

    prompt = f"""Based on this expense information, suggest the most appropriate expense category:

Vendor: {expense.vendor}
Items: {items_text}
Total Amount: {expense.currency} {expense.total_amount:.2f}

Common categories: Office Supplies, Travel, Meals & Entertainment, Software, Hardware, Professional Services, Utilities, Marketing, Training, Other.

Return ONLY the category name, nothing else."""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You categorize expenses based on vendor and item descriptions.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=20,
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()


def analyze_invoice_patterns(invoices: List[InvoiceExtraction]) -> Dict[str, Any]:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=api_key)

    summary_data = []
    for inv in invoices[:10]:
        vendor = str(inv.vendor_name.value) if inv.vendor_name.value else "Unknown"
        total = float(inv.invoice_total.value) if inv.invoice_total.value else 0.0
        summary_data.append(f"- {vendor}: ${total:.2f}")

    prompt = f"""Analyze these invoice patterns:

Recent Invoices:
{chr(10).join(summary_data)}

Total invoices analyzed: {len(invoices)}

Provide a brief analysis of spending patterns, frequent vendors, and any observations."""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You analyze financial patterns from invoice data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=250,
        temperature=0.3,
    )

    return {
        "analysis": response.choices[0].message.content,
        "invoice_count": len(invoices),
        "model_used": "mistral-small-latest",
    }
