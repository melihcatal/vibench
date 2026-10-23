from document_client import get_google_gemini_client
from document_models import ExpenseDocument


def summarize_invoice(expense_document: ExpenseDocument) -> str:
    gemini_model = get_google_gemini_client()

    summary_prompt = (
        f"Summarize the following invoice details:\n"
        f"Vendor: {expense_document.vendor_name}\n"
        f"Date: {expense_document.document_date}\n"
        f"Total: {expense_document.total_amount} {expense_document.currency}\n"
        f"Line Items: {len(expense_document.line_items)} items\n"
        "Provide a concise summary."
    )

    response = gemini_model.generate_content(summary_prompt)
    return response.text
