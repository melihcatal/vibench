import os
from document_client import get_documentai_client
from document_models import DocumentContent, KeyValueExtractionResult
from google.cloud import documentai_v1 as documentai


def extract_key_values(
    doc_content: DocumentContent, project_id: str, location: str, processor_id: str
) -> KeyValueExtractionResult:
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=doc_content.content, mime_type=doc_content.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    key_value_pairs = {}
    for entity in result.document.entities:
        if entity.type_ == "form_field":
            key = client.decode_text(
                entity.page_anchor, result.document.text
            )  # Example, usually entities have text_anchor for key/value
            value = client.decode_text(entity.text_anchor, result.document.text)
            key_value_pairs[key] = value
        elif (
            entity.type_ == "field_name"
        ):  # For robust key-value extraction, often an entity's text_anchor is the value
            key = client.decode_text(entity.text_anchor, result.document.text)
            if entity.bounding_poly and entity.bounding_poly.vertices:
                # Attempt to find the corresponding field_value by proximity or hierarchical structure if available
                # This is a simplified approach; real-world might involve more complex logic based on Document AI output structure
                value = ""
                for prop in entity.properties:
                    if prop.type_ == "field_value":
                        value = client.decode_text(
                            prop.text_anchor, result.document.text
                        )
                        break
                key_value_pairs[key] = value

    # More accurate extraction using form_field entities that have a `mention_text` for key and `normalized_value` or `text_anchor` for value
    # Iterate through entities to find form fields (key-value pairs)
    for entity in result.document.entities:
        if entity.type_ == "form_field":
            # The text_anchor or mention_text for the field name (key)
            key = ""
            if entity.mention_text:
                key = entity.mention_text
            elif entity.text_anchor:
                key = client.decode_text(entity.text_anchor, result.document.text)

            # The text_anchor or normalized_value for the field value
            value = ""
            if entity.normalized_value and entity.normalized_value.text:
                value = entity.normalized_value.text
            elif entity.text_anchor:
                # If normalized_value is not present, sometimes the value is directly linked to an entity's text anchor
                # Or it might be a child entity. This requires careful inspection of Document AI output for your specific processor.
                # For simplicity, we'll try to get it from the child entities if 'value' is not already set.
                for prop in entity.properties:
                    if prop.type_ == "field_value":
                        value = client.decode_text(
                            prop.text_anchor, result.document.text
                        )
                        break

            if key and value:
                key_value_pairs[key] = value

    return KeyValueExtractionResult(key_value_pairs=key_value_pairs)


if __name__ == "main":
    # Example Usage (replace with actual values and file content)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"
    PROCESSOR_ID = os.environ.get(
        "GOOGLE_DOCUMENT_AI_FORM_PROCESSOR_ID"
    )  # Use a specific form processor (e.g., "form-parser")

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_FORM_PROCESSOR_ID environment variables."
        )
    else:
        with open(
            "path/to/your/document.pdf", "rb"
        ) as image:  # Replace with your document path
            content = image.read()
        doc = DocumentContent(content=content, mime_type="application/pdf")
        kv_result = extract_key_values(doc, PROJECT_ID, LOCATION, PROCESSOR_ID)
        print("Extracted Key-Value Pairs:", kv_result.key_value_pairs)
