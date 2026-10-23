import os
from document_models import NormalizedExpense
from vertexai.preview.language_models import TextGenerationModel # Provider-specific import

# Initialize Vertex AI client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in an environment with appropriate service account permissions.
# project = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or your specific project ID
# location = "us-central1" # Or your specific region
# vertexai.init(project=project, location=location)

def summarize_invoice(expense: NormalizedExpense) -> str:
    # Using a placeholder for Vertex AI initialization, assuming it's done globally or via a context manager.
    # For a real application, you would initialize it properly.
    # model = TextGenerationModel.from_pretrained("text-bison") # Old model
    model = TextGenerationModel.from_pretrained("gemini-pro") # Updated model

    prompt = f"""Summarize the following expense record in a concise sentence:

    Vendor: {expense.vendor_name}
    Date: {expense.transaction_date}
    Total Amount: {expense.total_amount} {expense.currency if expense.currency else ''}
    Category: {expense.category}
    Notes: {expense.notes if expense.notes else 'N/A'}
    Line Items:
    {'-' + '\\n-'.join([f'{item.description} (Qty: {item.quantity}, Amt: {item.amount})' for item in expense.line_items]) if expense.line_items else 'N/A'}

    Summary:"""

    try:
        response = model.predict(
            prompt,
            temperature=0.2,
            max_output_tokens=150,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing invoice with Vertex AI: {e}")
        return "Could not generate summary."
