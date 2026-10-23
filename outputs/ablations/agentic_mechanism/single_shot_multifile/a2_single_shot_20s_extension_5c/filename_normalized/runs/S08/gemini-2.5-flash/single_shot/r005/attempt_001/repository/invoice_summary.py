import json
from typing import Dict, Any
from document_client import get_cohere_client
from document_models import NormalizedExpense

def summarize_invoice_fields(expense_record: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using Cohere Summarize API.
    """
    cohere_client = get_cohere_client()

    summary_text_parts = [
        f"Expense Record ID: {expense_record['id']}",
        f"Document Type: {expense_record['document_type'].capitalize()}",
        f"Vendor: {expense_record['vendor_name']}",
        f"Date: {expense_record['transaction_date']}",
        f"Total Amount: {expense_record['currency']} {expense_record['total_amount']:.2f}",
    ]

    if expense_record.get('tax_amount') is not None:
        summary_text_parts.append(f"Tax: {expense_record['currency']} {expense_record['tax_amount']:.2f}")

    if expense_record['line_items']:
        summary_text_parts.append("\nLine Items:")
        for item in expense_record['line_items']:
            qty = f"{item['quantity']:.0f}x" if item['quantity'] else ""
            unit_price = f"@{item['unit_price']:.2f}" if item['unit_price'] else ""
            summary_text_parts.append(f"- {item['description']}: {qty}{unit_price} {expense_record['currency']} {item['amount']:.2f}")
    
    if expense_record.get('notes'):
        summary_text_parts.append(f"\nNotes: {expense_record['notes']}")

    document_text = "\n".join(summary_text_parts)

    try:
        response = cohere_client.summarize(
            text=document_text,
            length='short',
            format='paragraph',
            model='command',
            temperature=0.3
        )
        return response.summary
    except Exception as e:
        print(f"Error during summarization with Cohere: {e}")
        return f"Could not generate summary: {str(e)}. Original details: {document_text[:200]}..."
