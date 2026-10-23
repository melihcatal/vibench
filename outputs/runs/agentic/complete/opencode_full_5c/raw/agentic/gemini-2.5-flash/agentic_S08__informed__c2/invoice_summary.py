import json
from document_models import NormalizedExpense, SummaryResult
from document_client import get_gemini_client


def summarize_invoice_fields(expense_record: NormalizedExpense) -> SummaryResult:
    """
    Summarizes extracted invoice fields using Google Gemini API.
    """
    client = get_gemini_client()

    prompt_parts = [
        f"You are an AI assistant that summarizes expense records. "
        f"Given the following normalized expense record, generate a concise summary. "
        f"Highlight the vendor, total amount, and key line items if available.\n\n",
        f"Normalized Expense Record:\n{json.dumps(expense_record.__dict__, indent=2)}\n\n",
        "Generate a summary in a paragraph format.",
    ]

    response = client.generate_content(prompt_parts)
    return SummaryResult(summary=response.text.strip())
