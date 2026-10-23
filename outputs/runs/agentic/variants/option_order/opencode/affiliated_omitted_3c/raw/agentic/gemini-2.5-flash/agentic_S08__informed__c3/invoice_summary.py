import json
from typing import Dict, Any
from document_client import get_openai_client
from document_models import NormalizedExpense, InvoiceSummary


def summarize_invoice_fields(normalized_expense: NormalizedExpense) -> InvoiceSummary:
    openai_client = get_openai_client()

    # Prepare a concise representation of the normalized expense for the LLM
    expense_data_for_llm = {
        "document_type": normalized_expense.document_type,
        "vendor_name": normalized_expense.vendor_name,
        "transaction_date": normalized_expense.transaction_date,
        "total_amount": normalized_expense.total_amount,
        "currency": normalized_expense.currency,
        "line_items_count": len(normalized_expense.line_items)
        if normalized_expense.line_items
        else 0,
        "tax_amount": normalized_expense.tax_amount,
        "memo_field": normalized_expense.memo_field,
    }

    prompt = f"""Summarize the following expense record, focusing on key details like vendor, total amount, date, and any specific notes or line item counts. Extract key phrases related to the expense.\n\nExpense Record:\n{json.dumps(expense_data_for_llm, indent=2)}\n\nProvide the summary as a JSON object with two fields: 'summary_text' (string) and 'key_phrases' (list of strings)."""

    chat_completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at summarizing expense records and extracting key phrases. Output only a JSON object.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    summary_json_str = chat_completion.choices[0].message.content
    summary_data = json.loads(summary_json_str)

    return InvoiceSummary(
        summary_text=summary_data.get("summary_text", ""),
        key_phrases=summary_data.get("key_phrases", []),
    )
