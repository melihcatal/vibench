from google.cloud import documentai_v1 as documentai
import os

# --- Configuration for Google Cloud Document AI ---
# Replace with your actual Google Cloud Project ID, location, and processor ID
PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
LOCATION = "YOUR_PROCESSOR_LOCATION"  # e.g., "us" or "eu"
PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # e.g., "a1b2c3d4e5f6g7h8"
# --- End Configuration ---

def process_document_with_documentai(file_path: str, mime_type: str) -> documentai.Document:
    """
    Processes a document using Google Cloud Document AI.
    """
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    resource_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

def validate_document_fields(document: documentai.Document, required_fields: dict) -> dict:
    """
    Validates if required fields are present and meet confidence thresholds.
    """
    validation_results = {"overall_valid": True, "field_validations": []}
    
    document_fields = {field.type_: field for field in document.entities}

    for field_name, requirements in required_fields.items():
        is_present = field_name in document_fields
        field_validation = {
            "field_name": field_name,
            "is_present": is_present,
            "confidence_met": False,
            "actual_confidence": None,
            "required_confidence": requirements.get("min_confidence", 0.0)
        }

        if is_present:
            entity = document_fields[field_name]
            actual_confidence = entity.confidence
            field_validation["actual_confidence"] = actual_confidence

            if actual_confidence >= requirements.get("min_confidence", 0.0):
                field_validation["confidence_met"] = True
            else:
                validation_results["overall_valid"] = False
        else:
            validation_results["overall_valid"] = False
        
        validation_results["field_validations"].append(field_validation)

    return validation_results

if __name__ == "__main__":
    # Example Usage:
    # 1. Ensure you have authenticated to Google Cloud (e.g., `gcloud auth application-default login`)
    # 2. Replace placeholders for PROJECT_ID, LOCATION, and PROCESSOR_ID
    # 3. Replace 'path/to/your/document.pdf' with your document path
    # 4. Define your required fields and their minimum confidence scores

    # Example document path and mime type
    # IMPORTANT: Make sure to provide a real document path and MIME type for testing.
    # For example, if you have a PDF invoice:
    # DOCUMENT_PATH = "path/to/your/invoice.pdf"
    # MIME_TYPE = "application/pdf"
    DOCUMENT_PATH = "path/to/your/document.pdf" 
    MIME_TYPE = "application/pdf" # or "image/tiff", "image/jpeg", "image/png"

    # Define required fields and their minimum confidence thresholds
    # Example for an invoice:
    # REQUIRED_FIELDS = {
    #     "supplier_name": {"min_confidence": 0.7},
    #     "total_amount": {"min_confidence": 0.8},
    #     "invoice_date": {"min_confidence": 0.75},
    # }
    REQUIRED_FIELDS = {
        "document_type": {"min_confidence": 0.7},
        "document_id": {"min_confidence": 0.6},
    }

    if not os.path.exists(DOCUMENT_PATH):
        print(f"Error: Document not found at {DOCUMENT_PATH}")
        print("Please replace 'path/to/your/document.pdf' with a valid document path and ensure you have configured PROJECT_ID, LOCATION, and PROCESSOR_ID.")
    elif PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID" or LOCATION == "YOUR_PROCESSOR_LOCATION" or PROCESSOR_ID == "YOUR_PROCESSOR_ID":
        print("Error: Google Cloud Document AI configuration missing.")
        print("Please update PROJECT_ID, LOCATION, and PROCESSOR_ID in the script.")
    else:
        try:
            print(f"Processing document: {DOCUMENT_PATH}...")
            document_ai_result = process_document_with_documentai(DOCUMENT_PATH, MIME_TYPE)
            print("Document processed successfully by Document AI.")

            validation_results = validate_document_fields(document_ai_result, REQUIRED_FIELDS)

            print("
--- Validation Results ---")
            print(f"Overall Document Valid: {validation_results['overall_valid']}")
            for field_result in validation_results["field_validations"]:
                print(f"  Field: {field_result['field_name']}")
                print(f"    Present: {field_result['is_present']}")
                if field_result['is_present']:
                    print(f"    Confidence Met ({field_result['required_confidence']:.2f}): {field_result['confidence_met']} (Actual: {field_result['actual_confidence']:.2f})")
                else:
                    print(f"    Required Confidence: {field_result['required_confidence']:.2f} (Field not found)")

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure your Google Cloud credentials are set up correctly and the Document AI processor is configured and enabled for your project.")
