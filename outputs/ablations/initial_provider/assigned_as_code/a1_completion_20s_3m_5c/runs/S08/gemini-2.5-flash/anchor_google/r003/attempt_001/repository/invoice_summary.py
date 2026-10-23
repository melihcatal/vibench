from google.cloud import aiplatform

def summarize_invoice_fields(extracted_invoice_data, config=None):
    config = config or {}
    aiplatform.init(project=config["project_id"], location=config["location"])

    # Load the text generation model
    # Using the specific model name as required: "gemini-pro"
    model = aiplatform.preview.generative_models.GenerativeModel(config["model_name"])

    invoice_text = f"Invoice from {extracted_invoice_data.get('vendor', 'Unknown Vendor')} on {extracted_invoice_data.get('date', 'Unknown Date')}. "
    invoice_text += f"Total amount: {extracted_invoice_data.get('total', 'N/A')}. "
    
    if extracted_invoice_data.get('line_items'):
        invoice_text += "Line items include: "
        for item in extracted_invoice_data['line_items']:
            invoice_text += f"{item.get('description', 'N/A')} (Amount: {item.get('amount', 'N/A')}), "
        invoice_text = invoice_text.strip(', ') + "."

    prompt = f"Summarize the following invoice details concisely: {invoice_text}"

    response = model.generate_content(prompt)
    
    # Access the text from the candidate directly
    summary = response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content else "No summary available."
    return {"summary": summary}