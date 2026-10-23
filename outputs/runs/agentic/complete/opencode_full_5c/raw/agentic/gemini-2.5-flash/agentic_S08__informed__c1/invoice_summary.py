import json
from document_client import get_gemini_client
from document_models import NormalizedExpense
import google.generativeai as genai


def summarize_invoice_fields(expense: NormalizedExpense) -> str:
    model = get_gemini_client()

    prompt = f"""
    Summarize the following expense record in a concise paragraph, highlighting key details such as:
    - Document type
    - Vendor name
    - Transaction date
    - Total amount and currency
    - Number of line items (if any)
    - Any notes present

    Expense Record:
    {json.dumps(expense.dict(), indent=2)}
    
    Provide only the summary text.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
