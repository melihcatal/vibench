from google.cloud import aiplatform

def summarize_invoice_fields(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using a Google Cloud Vertex AI model.

    Args:
        invoice_data: A dictionary containing extracted invoice fields.
                      Expected keys: "vendor_name", "date", "total_amount", "line_items", "notes".

    Returns:
        A string containing the summary of the invoice fields.
    """
    aiplatform.init(project="YOUR_GCP_PROJECT_ID", location="YOUR_GCP_REGION")
    
    # Use a specific model, for example, "gemini-pro"
    model = aiplatform.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following invoice details concisely:
    Vendor: {invoice_data.get("vendor_name", "N/A")}
    Date: {invoice_data.get("date", "N/A")}
    Total Amount: {invoice_data.get("total_amount", "N/A")}
    Line Items: {invoice_data.get("line_items", "N/A")}
    Notes: {invoice_data.get("notes", "N/A")}

    Provide a short summary highlighting the key information.
    """

    response = model.generate_content(prompt)
    return response.text
