from google.cloud import aiplatform

def summarize_invoice_fields(invoice_data: dict) -> str:
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and region
    model = aiplatform.GenerativeModel("gemini-pro")

    prompt = "Summarize the following invoice fields:\n"
    for key, value in invoice_data.items():
        prompt += f"- {key}: {value}\n"
    prompt += "Provide a concise summary of the invoice."

    response = model.generate_content(prompt)
    return response.text
