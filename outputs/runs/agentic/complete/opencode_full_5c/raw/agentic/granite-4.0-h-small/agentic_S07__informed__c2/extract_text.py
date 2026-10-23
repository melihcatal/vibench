from google.cloud import documentai


def extract_text(document_image_path):
    """Extract plain text from a scanned document image using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    name = "projects/{project}/locations/{location}/processors/{processor}"  # TODO: set values
    with open(document_image_path, "rb") as image_file:
        image = documentai.Document.from_data(image_file.read())
    response = client.process_document(name=name, raw_document=image)
    return response.document.text
