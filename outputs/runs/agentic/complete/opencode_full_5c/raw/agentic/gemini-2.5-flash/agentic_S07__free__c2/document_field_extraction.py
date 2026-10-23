from document_client import get_documentai_client, get_project_id, get_location
from document_models import DocumentKeyValueExtractionResponse, DocumentKeyValueEntry
from google.cloud import documentai_v1beta3 as documentai
import os


def extract_structured_fields_from_document(
    document_content: bytes, mime_type: str
) -> DocumentKeyValueExtractionResponse:
    project_id = get_project_id()
    location = get_location()
    # Use a pre-trained processor like 'Form Parser' or a custom processor for structured field extraction
    processor_id = os.getenv(
        "DOCUMENT_AI_FIELD_EXTRACTION_PROCESSOR_ID",
        "YOUR_FIELD_EXTRACTION_PROCESSOR_ID",
    )

    if processor_id == "YOUR_FIELD_EXTRACTION_PROCESSOR_ID":
        raise ValueError(
            "DOCUMENT_AI_FIELD_EXTRACTION_PROCESSOR_ID environment variable not set or is default. Please configure your Document AI field extraction processor ID."
        )

    client = get_documentai_client()

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_values = []
    for entity in document.entities:
        # For generic form parser, entities often represent key-value pairs
        if entity.type_ and entity.mention_text and entity.normalized_value:
            key_values.append(
                DocumentKeyValueEntry(
                    key=entity.type_,
                    value=entity.mention_text,  # Using mention_text as the value for now, consider normalized_value for processed data
                )
            )
        elif entity.type_ == "form_field":
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

            if key and value:
                key_values.append(
                    DocumentKeyValueEntry(key=key.strip(), value=value.strip())
                )

    return DocumentKeyValueExtractionResponse(key_values=key_values)
