from document_client import create_document_ai_client


def invoice_summary(extracted_invoice: dict) -> str:
    client = create_document_ai_client()
    prompt = {"task": "summarize_invoice", "invoice": extracted_invoice}
    response = client.models.generate_content(model="gemini-1.5-pro", contents=str(prompt))
    return getattr(response, "text", str(response))
