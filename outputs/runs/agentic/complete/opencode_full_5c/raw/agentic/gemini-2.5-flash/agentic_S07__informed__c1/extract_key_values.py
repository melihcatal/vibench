from google.cloud import documentai_v1b3 as documentai
import os


def extract_key_values(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """Extracts key-value pairs from a document using Google Document AI."""
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = document.text[
                form_field.field_name.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_name.text_anchor.text_segments[
                    0
                ].end_index
            ]
            field_value = document.text[
                form_field.field_value.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_value.text_anchor.text_segments[
                    0
                ].end_index
            ]
            key_value_pairs.append(
                {"key": field_name.strip(), "value": field_value.strip()}
            )
    return key_value_pairs


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # Create a "Form Parser" in Document AI
    FILE_PATH = "path/to/your/document_with_form.pdf"

    if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
        extracted_key_values = extract_key_values(
            PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH
        )
        print("Extracted Key-Value Pairs:\n", extracted_key_values)
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT, PROCESSOR_ID, and provide a valid FILE_PATH."
        )
