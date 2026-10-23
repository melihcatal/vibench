import google.generativeai as genai


def translate_invoice_notes(invoice_notes):
    genai.configure(api_key="your-api-key")
    model = genai.GenerativeModel("models/gemini-pro")
    response = model.generate_content(invoice_notes)
    return response.text
