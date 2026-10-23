from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_layout(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
    """
    Extracts layout elements (blocks, lines, tables) from a document using Google Cloud Document AI.
    """
    # You can set the api_endpoint if your project is not in "us"
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Document as bytes
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # For a full list of document object properties, please reference:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document

    # Extract text
    text = document.text

    # Extract pages and their layout elements
    # For example, to get all paragraphs
    paragraphs = []
    for page in document.pages:
        for paragraph in page.paragraphs:
            paragraphs.append(paragraph)
            
    # For example, to get all tables
    tables = []
    for page in document.pages:
        for table in page.tables:
            tables.append(table)

    return {"text": text, "paragraphs": paragraphs, "tables": tables}
