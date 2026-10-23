import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path

def extract_key_value_pairs(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts key-value pairs from a document using Google Document AI's Form Parser."""
    client = get_documentai_client()
    # For key-value extraction, it's often best to use a specialized form parser.
    # The processor_id here should correspond to a 'Form Parser' processor.
    processor_path = get_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    doc = response.document

    key_value_pairs = {}

    for entity in doc.entities:
        if entity.type == "form_field":
            key = ""
            value = ""
            if entity.text_anchor.text_segments:
                key = doc.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index]
            if entity.mention_text_anchor.text_segments:
                value = doc.text[entity.mention_text_anchor.text_segments[0].start_index:entity.mention_text_anchor.text_segments[0].end_index]
            key_value_pairs[key] = value
        # Document AI's specialized processors (like Invoice Parser) provide richer 'entities'
        # which might not directly be 'form_field' but would still represent key-value info.
        # For a general form parser, 'form_field' is common.

    return key_value_pairs

if __name__ == '__main__':
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOCATION = "us"
    # Use a Form Parser Processor ID or a specialized processor like 'form-parser-v2.0-2022-09-18'
    PROCESSOR_ID = os.getenv("DOCUMENTAI_FORM_PROCESSOR_ID", "your-form-processor-id") # e.g., "form-parser-v2.0-2022-09-18"
    SAMPLE_FILE = "path/to/your/form_document.pdf"

    # kv_pairs = extract_key_value_pairs(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_FILE)
    # for key, value in kv_pairs.items():
    #     print(f"Key: {key}, Value: {value}")
