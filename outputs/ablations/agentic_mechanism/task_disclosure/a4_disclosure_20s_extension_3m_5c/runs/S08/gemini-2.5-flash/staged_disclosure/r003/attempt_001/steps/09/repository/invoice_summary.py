
from google.cloud import aiplatform

def summarize_invoice(invoice_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud Vertex AI.

    Args:
        invoice_fields: A dictionary containing extracted invoice fields
                        (e.g., {"vendor_name": "ABC Corp", "total_amount": "100.00", "items": [...]}).

    Returns:
        A string summary of the invoice.
    """
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    location = "us-central1"  # Replace with your desired location

    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained text model for summarization
    # For example, 'text-bison@001' or a newer available model
    model_name = "text-bison@002"
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }

    # Construct the prompt for summarization
    # In a real scenario, you'd format invoice_fields into a coherent text for summarization
    invoice_text = f"Invoice details: Vendor Name: {invoice_fields.get('vendor_name', 'N/A')}, " \
                   f"Total Amount: {invoice_fields.get('total_amount', 'N/A')}, " \
                   f"Due Date: {invoice_fields.get('due_date', 'N/A')}. " \
                   f"Items: {invoice_fields.get('items', 'N/A')}."
    prompt = f"Summarize the following invoice details: {invoice_text}"

    try:
        response = aiplatform.predict(
            model_name=model_name,
            instances=[{"prompt": prompt}],
            parameters=parameters,
        )
        summary = response.predictions[0].content
        return summary
    except Exception as e:
        return f"Error summarizing invoice: {e}"

if __name__ == "__main__":
    # Example usage (replace with actual extracted invoice data)
    sample_invoice_fields = {
        "vendor_name": "Example Solutions Inc.",
        "total_amount": "150.75",
        "due_date": "2026-10-15",
        "items": [
            {"description": "Consulting Services", "quantity": 1, "unit_price": "100.00"},
            {"description": "Software License", "quantity": 1, "unit_price": "50.75"}
        ]
    }
    invoice_summary = summarize_invoice(sample_invoice_fields)
    print("Invoice Summary:")
    print(invoice_summary)
