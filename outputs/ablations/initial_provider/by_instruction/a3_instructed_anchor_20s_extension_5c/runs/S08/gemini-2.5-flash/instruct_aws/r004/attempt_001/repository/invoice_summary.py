import vertexai
from vertexai.preview.language_models import TextGenerationModel
from document_models import NormalizedExpense
from typing import Optional

def summarize_invoice_fields(normalized_expense: NormalizedExpense) -> Optional[str]:
    # Initialize Vertex AI
    vertexai.init(project="your-gcp-project-id", location="us-central1")
    model = TextGenerationModel.from_pretrained("gemini-pro")

    prompt = (
        f"Summarize the following expense record. "
        f"Document Type: {normalized_expense.document_type}. "
        f"Vendor: {normalized_expense.vendor_name or 'N/A'}. "
        f"Date: {normalized_expense.transaction_date or 'N/A'}. "
        f"Total Amount: {normalized_expense.total_amount or 'N/A'} {normalized_expense.currency or ''}. "
        f"Line Items: {normalized_expense.line_items}."
        f"Provide a concise summary highlighting key information."
    )

    try:
        response = model.predict(
            prompt,
            max_output_tokens=256,
            temperature=0.2,
            top_p=0.8,
            top_k=40,
        )
        return response.text
    except Exception as e:
        print(f"Error summarizing invoice: {e}")
        return None
