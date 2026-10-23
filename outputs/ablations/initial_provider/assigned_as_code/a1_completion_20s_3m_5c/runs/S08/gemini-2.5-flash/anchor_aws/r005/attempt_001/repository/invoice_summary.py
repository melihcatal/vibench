from typing import Dict, Any
from document_client import get_vertex_ai_prediction_client
import os

def summarize_invoice(extracted_invoice: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = config.get("gcp_location", os.environ.get("GCP_LOCATION", "us-central1"))
    
    client = get_vertex_ai_prediction_client(location=location)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-pro"

    # Construct the prompt for summarization
    prompt = f"Summarize the following invoice details:\n\n"
    prompt += f"Vendor: {extracted_invoice.get("vendor", {}).get("value", "N/A")}\n"
    prompt += f"Date: {extracted_invoice.get("date", {}).get("value", "N/A")}\n"
    prompt += f"Total: {extracted_invoice.get("total", {}).get("value", "N/A")}\n"
    if extracted_invoice.get("line_items"):
        prompt += "Line Items:\n"
        for item in extracted_invoice["line_items"]:
            prompt += f"- Description: {item.get("description", "N/A")}, Quantity: {item.get("quantity", "N/A")}, Amount: {item.get("amount", "N/A")}\n"

    instances = [{"prompt": prompt}]
    parameters = {"temperature": 0.2, "max_output_tokens": 200}

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    summary = ""
    if response.predictions:
        # Accessing the text from the response structure which might vary based on model output
        # Assuming a structure where the first prediction's content is the summary
        # This part might need adjustment based on the exact Vertex AI Gemini API response format
        # For simpler models, it might be directly response.predictions[0]['content'] or similar.
        # Let's assume the text is directly available in the prediction result.
        try:
            summary = response.predictions[0]["candidates"][0]["content"].get("parts")[0].get("text")
        except (KeyError, IndexError, AttributeError):
            summary = "Failed to generate summary."
            print("Warning: Unexpected Vertex AI Gemini API response format. Check documentation.")

    return {"summary": summary}
