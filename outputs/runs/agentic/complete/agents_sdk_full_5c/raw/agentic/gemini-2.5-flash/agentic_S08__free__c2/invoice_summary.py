import os
from typing import Union
from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1 import types
from document_client import DocumentClients, PROJECT_ID, LOCATION
from document_models import Invoice, NormalizedExpense

# Vertex AI model ID for Gemini Pro
GEMINI_PRO_MODEL_ID = os.environ.get("GEMINI_PRO_MODEL_ID", "gemini-pro")

def summarize_invoice_fields(document_data: Union[Invoice, NormalizedExpense]) -> str:
    """Summarizes extracted invoice fields using Google Cloud Vertex AI's Gemini Pro model.

    Args:
        document_data: An Invoice or NormalizedExpense dataclass instance.

    Returns:
        A string containing the summary.
    """
    client = DocumentClients.get_vertex_ai_prediction_client()

    # Construct the prompt for the generative model
    prompt_text = """
    Summarize the following expense document details concisely, highlighting the vendor/merchant, total amount, and key line items.

    """

    if isinstance(document_data, Invoice):
        prompt_text += f"Document Type: Invoice\n"
        prompt_text += f"Vendor: {document_data.vendor_name or 'N/A'}\n"
        prompt_text += f"Date: {document_data.invoice_date or 'N/A'}\n"
        prompt_text += f"Total: {document_data.total_amount or 'N/A'} {document_data.currency or ''}\n"
        if document_data.line_items:
            prompt_text += "Line Items:\n"
            for item in document_data.line_items:
                prompt_text += f"- {item.description or 'N/A'} (Qty: {item.quantity or 'N/A'}, Price: {item.total_amount or 'N/A'})\n"
    elif isinstance(document_data, NormalizedExpense):
        prompt_text += f"Document Type: {document_data.source_document_type.capitalize()}\n"
        prompt_text += f"Vendor/Merchant: {document_data.primary_vendor_merchant or 'N/A'}\n"
        prompt_text += f"Date: {document_data.transaction_date or 'N/A'}\n"
        prompt_text += f"Total Expense: {document_data.total_expense_amount or 'N/A'} {document_data.standardized_currency}\n"
        if document_data.expense_items:
            prompt_text += "Expense Items:\n"
            for item in document_data.expense_items:
                prompt_text += f"- {item.description or 'N/A'} (Qty: {item.quantity or 'N/A'}, Total: {item.total_amount or 'N/A'})\n"
    else:
        return "Invalid document data provided for summarization."

    instance = types.Instance(content=prompt_text)
    parameters = types.PredictRequest.Parameter(temperature=0.2, max_output_tokens=256)

    try:
        response = client.predict(
            endpoint=f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{GEMINI_PRO_MODEL_ID}",
            instances=[instance],
            parameters=parameters,
        )

        if response.predictions:
            # Assuming the prediction is a text response. The structure depends on the model output.
            summary = response.predictions[0]['content'] # Accessing content from the prediction structure
            return summary
        else:
            return "No summary could be generated."

    except Exception as e:
        print(f"Error summarizing with Vertex AI: {e}")
        return f"Error generating summary: {e}"
