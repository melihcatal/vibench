import os
from document_models import NormalizedExpense, SummaryResult
from document_client import get_vertex_ai_model
from vertexai.generative_models import GenerationConfig
import json

def summarize_invoice(normalized_expense: NormalizedExpense, config: dict = None) -> SummaryResult:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    model = get_vertex_ai_model(project_id, location, "gemini-1.5-flash-001")

    invoice_data_for_summary = {
        "vendor_name": normalized_expense.vendor_name,
        "transaction_date": normalized_expense.transaction_date,
        "total_amount": normalized_expense.total_amount,
        "currency": normalized_expense.currency,
        "description": normalized_expense.description,
        "line_items": [
            item.dict() for item in normalized_expense.line_items
        ]
    }

    prompt_text = f"Summarize the key information from this expense record, focusing on the vendor, total amount, date, and a brief overview of line items. Keep the summary concise and informative.\nExpense Record: {json.dumps(invoice_data_for_summary, indent=2)}"

    response = model.generate_content(
        [prompt_text],
        generation_config=GenerationConfig(temperature=0.4)
    )

    return SummaryResult(summary_text=response.text)
