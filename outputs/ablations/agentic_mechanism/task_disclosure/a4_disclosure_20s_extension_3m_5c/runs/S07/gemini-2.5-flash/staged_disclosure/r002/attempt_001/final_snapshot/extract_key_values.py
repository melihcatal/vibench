import os
from google.cloud import documentai_v1 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts key-value pairs from a form-like document using Google Cloud Document AI.
    
    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of the Document AI processor.
        file_path (str): The path to the document file.

    Returns:
        dict: A dictionary of extracted key-value pairs.
    """
    
    # Instantiate a Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF for now

    request = documentai.ProcessRequest(name=name, raw_document=document)

    # Process the document
    result = client.process_document(request=request)
    document_proto = result.document

    key_value_pairs = {}
    for page in document_proto.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content
            field_value = form_field.field_value.text_anchor.content
            key_value_pairs[field_name.strip()] = field_value.strip()

    return key_value_pairs

if __name__ == '__main__':
    # Replace with your actual project ID, location, and processor ID
    # You need to create a "Form Parser" processor in Google Cloud Document AI
    # and enable the Document AI API.
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "your-processor-id" # e.g., "your-processor-id"

    # Example usage:
    # Make sure you have a sample PDF document named "sample.pdf" in the same directory
    # or provide the correct path to your document.
    SAMPLE_DOCUMENT_PATH = "sample.pdf" 

    if not os.path.exists(SAMPLE_DOCUMENT_PATH):
        print(f"Error: Sample document '{SAMPLE_DOCUMENT_PATH}' not found.")
        print("Please create a sample.pdf file or update SAMPLE_DOCUMENT_PATH.")
    else:
        print(f"Extracting key-value pairs from {SAMPLE_DOCUMENT_PATH}...")
        extracted_data = extract_key_values(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_DOCUMENT_PATH)
        print("Extracted Key-Value Pairs:")
        for key, value in extracted_data.items():
            print(f"  {key}: {value}")
