import os
from typing import Dict, Any
from google.cloud import aiplatform


def summarize_invoice(extracted_invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    # Initialize Vertex AI
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained model for summarization
    # For this example, we'll use the Gemini Pro model
    model = aiplatform.preview.language_models.ChatModel.from_pretrained("gemini-pro")

    invoice = extracted_invoice_data.get("invoices", [{}])[0]
    vendor = invoice.get("vendor", "N/A")
    total = invoice.get("total", "N/A")
    date = invoice.get("date", "N/A")
    line_items = "\n".join([f"- {item.get('description')} (Qty: {item.get('quantity', 'N/A')}, Amt: {item.get('amount', 'N/A')})"
                            for item in invoice.get("line_items", [])])

    prompt = f"Summarize the following invoice details:\n\nVendor: {vendor}\nDate: {date}\nTotal: {total}\nLine Items:\n{line_items}\n\nProvide a concise summary highlighting the key information."

    response = model.predict(prompt)
    summary = response.text

    return {"summary": summary, "model_used": "gemini-pro", "provider": "Google Cloud Vertex AI"}