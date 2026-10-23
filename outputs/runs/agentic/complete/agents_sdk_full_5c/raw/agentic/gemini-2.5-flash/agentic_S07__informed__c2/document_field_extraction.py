import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions

def extract_structured_fields(document_content: bytes, mime_type: str, project_id: str, location: str, processor_id: str):
    """
    Extracts structured fields from an OCR-normalized document using Google Document AI.
    Specifically uses a pre-trained processor like 'invoice' or a custom processor.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_fields = []
    if document.entities:
        for entity in document.entities:
            field_value = None
            if entity.mention_text:
                field_value = entity.mention_text
            elif entity.normalized_value and entity.normalized_value.text:
                field_value = entity.normalized_value.text
            elif entity.properties:
                # Handle nested entities or complex types if needed
                field_value = [prop.type_ for prop in entity.properties] # Placeholder for complex value

            extracted_fields.append({
                "name": entity.type_,
                "value": field_value,
                "confidence": entity.confidence
            })
    return extracted_fields

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, project_id, location, processor_id and a document file)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us" # e.g., "us"
    # processor_id = "YOUR_PROCESSOR_ID" # e.g., for prebuilt-invoice, it might be a UUID
    #
    # with open("path/to/your/invoice.pdf", "rb") as image:
    #     document_content = image.read()
    # mime_type = "application/pdf"
    #
    # fields = extract_structured_fields(document_content, mime_type, project_id, location, processor_id)
    # for field in fields:
    #     print(f"Field: {field['name']}, Value: {field['value']}, Confidence: {field['confidence']}")
    pass
