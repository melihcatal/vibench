from google.cloud import documentai_v1 as documentai
import os


def extract_text(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts plain text from a document using Google Document AI.
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
    return result.document.text


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID"
    file_path = "path/to/your/document.pdf"  # Replace with your document path
    # print(extract_text(project_id, location, processor_id, file_path))
