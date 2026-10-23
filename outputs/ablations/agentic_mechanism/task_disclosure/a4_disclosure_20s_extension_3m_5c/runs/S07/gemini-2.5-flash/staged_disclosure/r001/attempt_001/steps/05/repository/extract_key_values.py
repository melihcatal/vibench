import os
from google.cloud import documentai_v1 as documentai

def extract_key_values_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> dict:
    """
    Extracts key-value pairs from a document using Google Cloud Document AI.
    
    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region (e.g., "us").
        processor_id (str): The ID of your Document AI processor.
        file_path (str): The local path to the document file.
        mime_type (str): The MIME type of the document (e.g., "application/pdf").
        
    Returns:
        dict: A dictionary containing the extracted key-value pairs.
    """
    
    # Instantiate a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(
        project_id, location, processor_id
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Create a Document object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Use the Document AI client to process the document
    result = documentai_client.process_document(request=request)
    
    document = result.document
    
    key_value_pairs = {}
    for entity in document.entities:
        if entity.type_ == "form_field":
            key = entity.mention_text
            value = ""
            if entity.normalized_value:
                value = entity.normalized_value.text
            elif entity.text_anchor:
                # Extract text using text_anchor if normalized_value is not available
                start_index = int(entity.text_anchor.text_segments[0].start_index)
                end_index = int(entity.text_anchor.text_segments[0].end_index)
                value = document.text[start_index:end_index]
            key_value_pairs[key] = value

    return key_value_pairs

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace with your actual project_id, location, processor_id, file_path, and mime_type.
    # Make sure you have authenticated to Google Cloud and enabled the Document AI API.
    
    # For authentication, you can use:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    # location = "us"  # e.g., "us"
    # processor_id = "YOUR_PROCESSOR_ID"  # Create a "Form Parser" processor in Document AI
    # file_path = "path/to/your/form.pdf"
    # mime_type = "application/pdf"

    # if not all([project_id, processor_id, file_path, mime_type]):
    #     print("Please set GOOGLE_CLOUD_PROJECT_ID, YOUR_PROCESSOR_ID, file_path, and mime_type.")
    # else:
    #     extracted_data = extract_key_values_from_document(
    #         project_id, location, processor_id, file_path, mime_type
    #     )
    #     print("Extracted Key-Value Pairs:")
    #     for key, value in extracted_data.items():
    #         print(f"{key}: {value}")
    print("File 'extract_key_values.py' created with Google Cloud Document AI integration.")
