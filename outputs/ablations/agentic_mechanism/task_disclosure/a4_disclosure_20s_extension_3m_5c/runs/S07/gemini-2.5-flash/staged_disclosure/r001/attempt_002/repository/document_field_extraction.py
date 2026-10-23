from google.cloud import documentai_v1 as documentai
import os

def extract_fields_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
):
    """
    Extracts structured fields from a document using Google Cloud Document AI.
    """
    documentai_client = documentai.DocumentProcessorServiceClient()
    
    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    
    document = result.document
    
    # For a general processor, entities contain the extracted fields.
    # For a specialized parser, the structure of the document object might be different.
    extracted_fields = []
    if document.entities:
        for entity in document.entities:
            field_info = {
                "type": entity.type,
                "mention_text": entity.mention_text,
                "confidence": entity.confidence
            }
            extracted_fields.append(field_info)
            
    return extracted_fields

if __name__ == "__main__":
    # Replace with your actual project ID, location, and processor ID
    # For example, a "Form Parser" processor
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-project-id")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "your-processor-id"  # e.g., "your-processor-id"
    
    # Replace with the path to your document and its MIME type
    DOCUMENT_FILE_PATH = "path/to/your/document.pdf"  # e.g., "document.pdf"
    DOCUMENT_MIME_TYPE = "application/pdf"  # e.g., "application/pdf", "image/tiff"

    # Example usage:
    # try:
    #     fields = extract_fields_from_document(
    #         PROJECT_ID, LOCATION, PROCESSOR_ID, DOCUMENT_FILE_PATH, DOCUMENT_MIME_TYPE
    #     )
    #     if fields:
    #         print("Extracted Fields:")
    #         for field in fields:
    #             print(f"  Type: {field['type']}, Text: {field['mention_text']}, Confidence: {field['confidence']:.2f}")
    #     else:
    #         print("No fields extracted.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    print("Please configure your GOOGLE_CLOUD_PROJECT_ID, LOCATION, PROCESSOR_ID, DOCUMENT_FILE_PATH, and DOCUMENT_MIME_TYPE.")
    print("Uncomment the example usage section to run the extraction.")
