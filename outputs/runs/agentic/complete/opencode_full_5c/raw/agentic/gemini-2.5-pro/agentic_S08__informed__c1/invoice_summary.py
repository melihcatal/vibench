import os
import google.generativeai as genai
from document_models import NormalizedExpense


def invoice_summary(expense: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        f"Summarize the following expense in a single sentence. "
        f"Vendor: {expense.vendor}, Date: {expense.transaction_date}, Total: ${expense.total:.2f}"
    )

    response = model.generate_content(prompt)
    return response.text
