from google.cloud import documentai_v1 as documentai
import os


def run_ocr_on_stored_document(
    project_id: str, location: str, processor_id: str, gcs_input_uri: str
) -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    input_config = documentai.DocumentInputConfig(
        gcs_source=documentai.GcsSource(uri=gcs_input_uri)
    )

    request = documentai.ProcessRequest(name=name, input_config=input_config)

    result = client.process_document(request=request)
    document = result.document

    return {
        "text": document.text,
        "pages": [
            {
                "page_number": page.page_number,
                "dimension": {
                    "width": page.dimension.width,
                    "height": page.dimension.height,
                    "unit": page.dimension.unit,
                },
            }
            for page in document.pages
        ],
    }
