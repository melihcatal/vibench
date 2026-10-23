from google.cloud import documentai_v1 as documentai
import os

def extract_structured_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts structured fields (e.g., from invoices) using Google Document AI pre-built processors."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {}
    for entity in document.entities:
        # For pre-built processors like Invoice Parser, entities directly represent fields.
        # entity.type_ will be like 'invoice_id', 'total_amount', etc.
        # entity.mention_text contains the extracted value.
        field_value = entity.mention_text
        if field_value:
            extracted_fields[entity.type_] = field_value
        elif entity.normalized_value: # For structured values like dates, numbers
            extracted_fields[entity.type_] = entity.normalized_value.text
    
    return extracted_fields

if __name__ == '__main__':
    # Placeholder values for demonstration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"
    PROCESSOR_ID = "your-invoice-parser-processor-id" # Use an Invoice Parser processor
    FILE_PATH = "path/to/your/invoice.pdf"

    # fields = extract_structured_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # print("Extracted Fields:")
    # for key, value in fields.items():
    #     print(f"  {key}: {value}")
