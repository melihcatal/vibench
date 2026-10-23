from google.cloud import documentai_v1 as documentai
import os

def extract_key_values_from_form(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> documentai.Document:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI Form Parser.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of a Form Parser processor (e.g., "FORM_PARSER_ID").
        file_content: The content of the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

    Returns:
        A Document object containing the extracted key-value pairs (entities).
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    # Refer to https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors/process
    # The processor_id should correspond to a "Form Parser" processor.
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)
    return result.document

if __name__ == '__main__':
    # Example usage placeholder
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    # location = "us"
    # processor_id = "your-form-parser-processor-id" 
    # with open("path/to/form.pdf", "rb") as f:
    #     content = f.read()
    # doc = extract_key_values_from_form(project_id, location, processor_id, content, "application/pdf")
    # print(f"Document Text: {doc.text[:200]}...")
    # if doc.entities:
    #     print("Extracted Entities (Key-Value Pairs):")
    #     for entity in doc.entities:
    #         if entity.type_ == "form_field" and entity.mention_text and entity.normalized_value.text:
    #             print(f"  Key: {entity.mention_text}, Value: {entity.normalized_value.text}")
    pass
