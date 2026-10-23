
from google.cloud import documentai_v1 as documentai

def validate_document_fields(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
    """
    Validates required structured fields and their confidence scores using Google Cloud Document AI.
    """

    # Initialize client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)
    document = result.document

    print(f"Document processing complete.")

    # Example: Validate specific fields and their confidence scores
    required_fields = {
        "invoice_id": 0.9,  # Field name and minimum confidence score
        "total_amount": 0.8,
    }

    found_fields = {}
    for entity in document.entities:
        if entity.type_ in required_fields:
            found_fields[entity.type_] = {
                "value": entity.mention_text,
                "confidence": entity.confidence
            }

    print("\n--- Field Validation Results ---")
    all_fields_valid = True
    for field_name, min_confidence in required_fields.items():
        if field_name not in found_fields:
            print(f"Field '{field_name}' MISSING.")
            all_fields_valid = False
        else:
            field_info = found_fields[field_name]
            print(f"Field '{field_name}': Value='{field_info['value']}', Confidence={field_info['confidence']:.2f}")
            if field_info['confidence'] < min_confidence:
                print(f"  Confidence for '{field_name}' is BELOW threshold ({min_confidence:.2f}).")
                all_fields_valid = False

    if all_fields_valid:
        print("\nAll required fields are present and meet confidence thresholds.")
    else:
        print("\nSome required fields are missing or have low confidence.")

    return all_fields_valid

if __name__ == "__main__":
    # TODO: Replace with your actual Google Cloud project ID, location, and processor ID
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "your-processor-id"  # e.g., "YOUR_PROCESSOR_ID"

    # TODO: Replace with the path to your document and its MIME type
    # Example for a PDF invoice
    FILE_PATH = "path/to/your/document.pdf"
    MIME_TYPE = "application/pdf"

    # Example for a JPG image
    # FILE_PATH = "path/to/your/image.jpg"
    # MIME_TYPE = "image/jpeg"

    print("Please ensure you have authenticated with Google Cloud and have the necessary permissions.")
    print("Also, ensure you have replaced the placeholder values for PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, and MIME_TYPE.")

    try:
        # result = validate_document_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, MIME_TYPE)
        print("\nUncomment the call to validate_document_fields and provide actual values to run the validation.")
    except Exception as e:
        print(f"An error occurred: {e}")
