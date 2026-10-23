from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import os

def stored_document_ocr(payload):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., 'us' or 'eu'
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID")
    
    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud Project ID, Location, or Document AI Processor ID not found in environment variables.")

    # The GCS URI of the input document, e.g., "gs://cloud-samples-data/documentai/invoice.pdf"
    gcs_input_uri = payload['gcs_input_uri']

    # Online processing request to Document AI
    documentai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    )

    name = documentai_client.processor_path(project_id, location, processor_id)

    # Configure the process request
    input_config = documentai.Document.to_dict()
    input_config["gcs_source"] = gcs_input_uri
    input_config = documentai.Document.from_json(str(input_config))

    request = documentai.ProcessRequest(
        name=name,
        document=input_config
    )

    result = documentai_client.process_document(request)
    
    # For this example, we'll just extract the text.
    # More complex parsing would involve iterating through entities, pages, etc.
    return {'text_content': result.document.text, 'gcs_input_uri': gcs_input_uri}
