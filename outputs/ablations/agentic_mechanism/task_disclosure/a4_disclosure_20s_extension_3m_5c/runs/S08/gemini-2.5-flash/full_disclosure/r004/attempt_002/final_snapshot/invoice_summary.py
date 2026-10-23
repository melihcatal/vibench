import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationConfig

def summarize_invoice_fields(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud's Generative AI.

    Args:
        invoice_data (dict): A dictionary containing extracted invoice fields.
                             Expected keys: 'vendor_name', 'invoice_date', 'total_amount', 'line_items'.
                             Line items should be a list of dictionaries with 'description' and 'amount'.

    Returns:
        str: A summary of the invoice fields.
    """
    vertexai.init(project="your-gcp-project-id", location="your-gcp-region") # Replace with your GCP project ID and region
    model = GenerativeModel("gemini-pro")

    prompt = "Summarize the following invoice details:\n"
    if invoice_data.get("vendor_name"):
        prompt += f"- Vendor: {invoice_data["vendor_name"]}\n"
    if invoice_data.get("invoice_date"):
        prompt += f"- Date: {invoice_data["invoice_date"]}\n"
    if invoice_data.get("total_amount"):
        prompt += f"- Total Amount: {invoice_data["total_amount"]}\n"
    
    line_items = invoice_data.get("line_items")
    if line_items:
        prompt += "Line Items:\n"
        for item in line_items:
            description = item.get("description", "N/A")
            amount = item.get("amount", "N/A")
            prompt += f"  - {description}: {amount}\n"
    
    prompt += "\nProvide a concise summary highlighting the key information."

    generation_config = GenerationConfig(
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )

    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    return response.text
