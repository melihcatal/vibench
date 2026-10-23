from google.cloud import documentai_v1 as documentai
import os

def extract_key_value_pairs(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts key-value pairs from a document using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for entity in document.entities:
        if entity.type == "form_field":
            key_text = ""
            if entity.page_anchor.page_refs:
                for segment in entity.page_anchor.page_refs[0].text_segments:
                    key_text += document.text[segment.start_index:segment.end_index]

            value_text = ""
            for prop in entity.properties:
                if prop.type == "value":
                    if prop.page_anchor.page_refs:
                        for segment in prop.page_anchor.page_refs[0].text_segments:
                            value_text += document.text[segment.start_index:segment.end_index]
            
            if key_text or value_text: # Ensure there's at least a key or value
                key_value_pairs.append({"key": key_text.strip(), "value": value_text.strip()})

    # The above extraction logic is a bit generic for 'form_field'.
    # For robust key-value extraction, a specialized processor like "Form Parser" is best.
    # The entities directly contain key-value pairs when using appropriate processors.
    # A more direct approach for Form Parser output:
    for entity in document.entities:
        if entity.type_ == "form_field":
            key = documentai.get_text_from_element(entity.text_anchor, document)
            value = documentai.get_text_from_element(entity.value_anchor, document)
            key_value_pairs.append({"key": key, "value": value})


    return key_value_pairs

if __name__ == '__main__':
    # Placeholder values for demonstration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"
    PROCESSOR_ID = "your-form-parser-processor-id" # Use a Form Parser processor
    FILE_PATH = "path/to/your/document.pdf"

    # kvs = extract_key_value_pairs(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # for kv in kvs:
    #     print(f"Key: '{kv['key']}', Value: '{kv['value']}'")
