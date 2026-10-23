import google.generativeai as genai
from typing import Dict, Any
from document_models import NormalizedExpense
from document_client import load_config

def summarize_invoice_fields(normalized_expense_data: Dict[str, Any]) -> Dict[str, Any]:
    config = load_config()
    model_name = config.get("google_generative_model_name")

    if not model_name:
        raise ValueError("Google Generative AI model name is not configured.")

    # Ensure GOOGLE_API_KEY environment variable is set for genai
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY environment variable not set for Google Generative AI.")

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    normalized_expense = NormalizedExpense(**normalized_expense_data["normalized_expense"])

    summary_prompt = f"""
    Summarize the following expense record:
    Document Type: {normalized_expense.document_type}
    Vendor Name: {normalized_expense.vendor_name}
    Transaction Date: {normalized_expense.transaction_date}
    Total Amount: {normalized_expense.total_amount}
    Tax Amount: {normalized_expense.tax_amount}
    Line Items: {normalized_expense.line_items}

    Provide a concise summary in a single paragraph.
    """

    response = model.generate_content(summary_prompt)
    summary = response.text

    return {"summary": summary}
