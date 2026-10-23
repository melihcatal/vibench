import os
from document_client import get_openai_client
from document_models import ExtractedInvoiceFields
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

def extract_invoice_fields(invoice_text: str) -> ExtractedInvoiceFields:
    client = get_openai_client()
    system_message = ChatCompletionSystemMessageParam(content="""You are an AI assistant specialized in extracting structured data from invoice documents.
    Extract the vendor name, invoice date, total amount, and line items (description, quantity, unit price, total price) from the provided invoice text.
    If a field is not found, leave it as None. For line items, extract as much detail as possible.
    Respond only with a JSON object conforming to the ExtractedInvoiceFields schema.
    """, role="system")

    user_message = ChatCompletionUserMessageParam(content=invoice_text, role="user")

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_INVOICE_MODEL_NAME", "gpt-4"),
        messages=[
            system_message,
            user_message,
        ],
        response_format={"type": "json_object"}
    )
    
    extracted_data = response.choices[0].message.content
    return ExtractedInvoiceFields.model_validate_json(extracted_data)
