import os
from typing import Dict, Any
import google.generativeai as genai
from document_models import NormalizedExpense
from document_client import load_config

def summarize_invoice_fields(expense_record: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud Generative AI (Gemini Pro).
    """
    config = load_config("gemini")
    api_key = config.get("api_key")
    model_name = config.get("model_name")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    Summarize the following invoice expense record in a concise paragraph. 
    Highlight the vendor, total amount, and key line items if present.

    Vendor: {expense_record.vendor_name}
    Transaction Date: {expense_record.transaction_date}
    Total Amount: {expense_record.total_amount} {expense_record.currency}
    Line Items: {', '.join([f'{{item.description}} ({{item.amount}})' for item in expense_record.line_items]) if expense_record.line_items else 'No specific line items mentioned.'}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example Usage
    from document_models import LineItem

    os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
    os.environ["GEMINI_MODEL_NAME"] = "gemini-pro"

    example_invoice = NormalizedExpense(
        document_type="invoice",
        vendor_name="Global Supplies Co.",
        transaction_date="2023-03-10",
        total_amount=575.20,
        tax_amount=45.20,
        currency="EUR",
        line_items=[
            LineItem(description="Office Chairs", quantity=2.0, unit_price=150.00, amount=300.00),
            LineItem(description="Desk Lamps", quantity=3.0, unit_price=75.00, amount=225.00),
        ],
        notes="Urgent delivery requested for project XYZ."
    )

    summary = summarize_invoice_fields(example_invoice)
    print("Generated Invoice Summary:", summary)
