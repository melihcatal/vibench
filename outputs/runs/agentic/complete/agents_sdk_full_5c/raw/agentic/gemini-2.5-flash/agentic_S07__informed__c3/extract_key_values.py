import os
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    This typically requires a specialized form parser processor.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    
    key_value_pairs = []
    # Form fields are usually present if a specialized form parser is used.
    # For a general processor, fields might be empty or require more advanced post-processing.
    for entity in result.document.entities:
        if entity.type_ == "form_field": # This type is often used for key-value pairs
            key = result.document.get_text(entity.page_anchor.page_refs[0].layout)
            value = result.document.get_text(entity.mention_text_anchor.text_segments[0].end_index)
            key_value_pairs.append({"key": key.strip(), "value": value.strip()})
        elif entity.type_ == "document_field": # Another common type for extracted fields
            key_value_pairs.append({
                "field_name": entity.type_,
                "mention_text": result.document.get_text(entity.text_anchor),
                "normalized_value": entity.normalized_value.text if entity.normalized_value else None
            })

    return key_value_pairs

if __name__ == '__main__':
    # Placeholder for direct execution
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_FORM") # A specialized form parser processor

    # Example: kvs = extract_key_values(project_id, location, processor_id, "path/to/your/form.pdf")
    # print("Extracted Key-Value Pairs:", kvs)
