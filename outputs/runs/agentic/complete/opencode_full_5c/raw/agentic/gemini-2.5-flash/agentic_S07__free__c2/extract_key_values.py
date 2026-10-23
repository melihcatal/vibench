from document_client import get_documentai_client, get_project_id, get_location
from document_models import DocumentKeyValueExtractionResponse, DocumentKeyValueEntry
from google.cloud import documentai_v1beta3 as documentai
import os


def extract_key_values_from_document(
    document_content: bytes, mime_type: str
) -> DocumentKeyValueExtractionResponse:
    project_id = get_project_id()
    location = get_location()
    # Replace with your actual processor ID for form parsing
    processor_id = os.getenv("DOCUMENT_AI_FORM_PROCESSOR_ID", "YOUR_FORM_PROCESSOR_ID")

    if processor_id == "YOUR_FORM_PROCESSOR_ID":
        raise ValueError(
            "DOCUMENT_AI_FORM_PROCESSOR_ID environment variable not set or is default. Please configure your Document AI form processor ID."
        )

    client = get_documentai_client()

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_values = []
    for entity in document.entities:
        if entity.type_ == "form_field":  # This is specific to form parser output
            key = ""
            value = ""
            if entity.page_anchor and entity.page_anchor.page_refs:
                for page_ref in entity.page_anchor.page_refs:
                    if (
                        page_ref.layout
                        and page_ref.layout.text_anchor
                        and page_ref.layout.text_anchor.text_segments
                    ):
                        key += "".join(
                            [
                                text_segment.text_content
                                for text_segment in page_ref.layout.text_anchor.text_segments
                            ]
                        )

            if entity.properties:
                for prop in entity.properties:
                    if (
                        prop.type_ == "value"
                        and prop.page_anchor
                        and prop.page_anchor.page_refs
                    ):
                        for page_ref in prop.page_anchor.page_refs:
                            if (
                                page_ref.layout
                                and page_ref.layout.text_anchor
                                and page_ref.layout.text_anchor.text_segments
                            ):
                                value += "".join(
                                    [
                                        text_segment.text_content
                                        for text_segment in page_ref.layout.text_anchor.text_segments
                                    ]
                                )

            if key and value:  # Only add if both key and value are found
                key_values.append(
                    DocumentKeyValueEntry(key=key.strip(), value=value.strip())
                )

    return DocumentKeyValueExtractionResponse(key_values=key_values)
