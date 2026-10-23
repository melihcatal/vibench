import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

def summarize_invoice(invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Google's Gemini-Pro model.

    Args:
        invoice_data: A dictionary containing extracted invoice fields.

    Returns:
        A string containing the summary of the invoice.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1")
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Please summarize the following invoice data:

    Vendor: {invoice_data.get("vendor", "N/A")}
    Date: {invoice_data.get("date", "N/A")}
    Total: {invoice_data.get("total", "N/A")}
    Line Items:
    """
    if "line_items" in invoice_data:
        for item in invoice_data["line_items"]:
            prompt += f"""
            - Description: {item.get("description", "N/A")}, Quantity: {item.get("quantity", "N/A")}, Unit Price: {item.get("unit_price", "N/A")}, Amount: {item.get("amount", "N/A")}"""
    else:
        prompt += "N/A"

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.4,
            top_p=0.8,
            top_k=40
        )
    )
    return response.text

