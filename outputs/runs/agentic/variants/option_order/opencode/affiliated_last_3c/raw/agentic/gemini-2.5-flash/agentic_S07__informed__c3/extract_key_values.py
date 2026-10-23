from google.cloud import documentai_v1 as documentai
import os


def extract_key_values(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    key_value_pairs = {}
    for entity in result.document.entities:
        if entity.type_ == "form_field":
            key = entity.mention_text
            value = (
                entity.normalized_value.text
                if entity.normalized_value
                else entity.text_anchor.text_segments[0].text_content
                if entity.text_anchor.text_segments
                else ""
            )
            key_value_pairs[key] = value

    return key_value_pairs


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID"
    file_path = "path/to/your/document.pdf"  # Replace with your document path
    # kvs = extract_key_values(project_id, location, processor_id, file_path)
    # import json
    # print(json.dumps(kvs, indent=2))
