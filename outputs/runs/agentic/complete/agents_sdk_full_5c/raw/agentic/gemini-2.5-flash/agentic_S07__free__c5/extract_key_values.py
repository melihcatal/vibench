import os
from google.cloud import documentai_v1 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> dict:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    key_value_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = ""
            if form_field.field_name.text_anchor.text_segments:
                start = int(form_field.field_name.text_anchor.text_segments[0].start_index)
                end = int(form_field.field_name.text_anchor.text_segments[0].end_index)
                field_name = document.text[start:end]

            field_value = ""
            if form_field.field_value.text_anchor.text_segments:
                start = int(form_field.field_value.text_anchor.text_segments[0].start_index)
                end = int(form_field.field_value.text_anchor.text_segments[0].end_index)
                field_value = document.text[start:end]
            
            if field_name:
                key_value_pairs[field_name.strip()] = field_value.strip()

    return key_value_pairs

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, processor, and file)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "YOUR_PROCESSOR_ID" # This should be a "Form Parser" processor
    #
    # if project_id and processor_id:
    #     with open("path/to/your/form.pdf", "rb") as form_file:
    #         content = form_file.read()
    #         mime_type = "application/pdf"
    #         kv_pairs = extract_key_values(project_id, location, processor_id, content, mime_type)
    #         print("Extracted Key-Value Pairs:", kv_pairs)
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT and provide a processor_id for a Form Parser.")
    pass
