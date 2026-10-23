from google.cloud import documentai


def extract_layout(document_image_path):
    """Extract blocks, lines, tables, and other layout elements from a document image using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    name = "projects/{project}/locations/{location}/processors/{processor}"  # TODO: set values
    with open(document_image_path, "rb") as image_file:
        image = documentai.Document.from_data(image_file.read())
    response = client.process_document(name=name, raw_document=image)
    return response.document
