from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from storage_models import OCRRequest

def run_ocr_on_stored_document(request: OCRRequest, project_id: str, location: str = "us") -> str:
    """Runs OCR on a stored document object using Google Document AI.

    Args:
        request: An OCRRequest object containing bucket and object names.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region for Document AI processor (e.g., "us").

    Returns:
        The extracted text from the document.
    """

    # The Document AI client libraries use regional endpoints, meaning that your
    # request is sent to a specific region. For example, us-central1.
    # For a full list of regional endpoints, see: https://cloud.google.com/document-ai/docs/regions
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # You must set the `project_id`, `location`, and `processor_id` parameters.
    # The `processor_id` for a pre-trained OCR processor is typically specific to the region.
    # For generic OCR, you might use 'ocr-v1', 'ocr-standard', etc., or a custom processor.
    # This example assumes a general OCR processor. You might need to create one 
    # in the Document AI console or use a well-known public processor ID.
    # Replace with your actual processor ID if you have a specific one.
    processor_id = "your-ocr-processor-id" # e.g., "a1b2c3d4e5f6g7h8"
    resource_name = client.processor_path(project_id, location, processor_id)

    gcs_document = documentai.GcsDocument(gcs_uri=f"gs://{request.bucket_name}/{request.object_name}", mime_type=request.mime_type)
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    # Configure the output for the batch process
    # Note: For batch processing, results are written to a GCS output location.
    # For simpler use cases or single document processing, you might use `process_document` instead.
    # However, `process_document` has size/page limits and is synchronous.
    # This example assumes batch processing for potentially larger documents.
    gcs_output_uri_prefix = f"gs://{request.bucket_name}/document_ai_output/"
    output_config = documentai.DocumentOutputConfig(gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(gcs_uri_prefix=gcs_output_uri_prefix))

    # Batch process the document
    operation = client.batch_process_documents(request=documentai.BatchProcessDocumentsRequest(
        name=resource_name,
        input_documents=input_config,
        document_output_config=output_config
    ))

    print("Waiting for operation to complete...")
    operation.result(timeout=1200)  # Wait for the operation to finish (timeout in seconds)

    # After the operation completes, you would typically read the results from the GCS output path.
    # This example does not include reading the parsed documents from GCS output, as it's a separate step.
    # For simplicity, we'll return a placeholder message. In a real scenario, you'd parse the output JSONs.
    extracted_text_placeholder = "OCR completed. Results are in GCS output path. Implement logic to read them."
    print(extracted_text_placeholder)
    return extracted_text_placeholder

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up and Document AI API is enabled.
    # Also, ensure you have a Document AI processor created and replace "your-ocr-processor-id".
    # project_id = "your-gcp-project-id"
    # bucket_name = "your-bucket-name"
    # object_name = "your-document.pdf"
    # ocr_request = OCRRequest(bucket_name=bucket_name, object_name=object_name, mime_type="application/pdf")
    # extracted_text = run_ocr_on_stored_document(ocr_request, project_id=project_id)
    # print(f"Extracted text: {extracted_text}")
    pass
