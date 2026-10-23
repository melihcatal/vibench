from google.cloud import documentai_v1b3 as documentai
import os


def extract_structured_fields(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """Extracts structured fields from a document using a specific Google Document AI processor (e.g., Invoice Parser, Receipt Parser)."""
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

    extracted_fields = {}
    for entity in document.entities:
        # Access fields based on the specific processor's schema
        # This is a generic example; actual field names and structures vary by processor
        if entity.type_ != "":
            value = (
                document.text[
                    entity.text_anchor.text_segments[
                        0
                    ].start_index : entity.text_anchor.text_segments[0].end_index
                ].strip()
                if entity.text_anchor.text_segments
                else entity.mention_text
            )
            extracted_fields[entity.type_] = value
    return extracted_fields


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = (
        "YOUR_SPECIALIZED_PROCESSOR_ID"  # e.g., an Invoice Parser processor ID
    )
    FILE_PATH = "path/to/your/invoice.pdf"

    if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
        structured_data = extract_structured_fields(
            PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH
        )
        print("Extracted Structured Data:\n", structured_data)
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT, PROCESSOR_ID, and provide a valid FILE_PATH."
        )
