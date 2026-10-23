import os
from typing import Dict, Any, List
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentInput, DocumentOutput


def extract_key_values_from_document(
    document_input: DocumentInput, project_id: str, location: str, processor_id: str
) -> DocumentOutput:
    """Extracts key-value pairs from a form-like document using Google Document AI.
    Requires a processor trained for form parsing or a pre-trained processor like 'Form Parser'.
    """
    client = get_documentai_client()
    processor_name = get_processor_name(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    response = client.process_document(request=request)
    document = response.document

    key_value_pairs: List[Dict[str, Any]] = []
    for entity in document.entities:
        if entity.type == "form_field":  # This type might vary based on processor
            key_value_pairs.append(
                {
                    "field_name": document.text[
                        entity.text_anchor.text_segments[
                            0
                        ].start_index : entity.text_anchor.text_segments[0].end_index
                    ]
                    if entity.text_anchor.text_segments
                    else "",
                    "field_value": document.text[
                        entity.normalized_value.text_anchor.text_segments[
                            0
                        ].start_index : entity.normalized_value.text_anchor.text_segments[
                            0
                        ].end_index
                    ]
                    if entity.normalized_value
                    and entity.normalized_value.text_anchor.text_segments
                    else entity.mention_text,
                }
            )
        elif (
            entity.type == "value"
        ):  # This is a common type for values without a direct 'form_field' parent
            # Attempt to find the corresponding key if available, or just store the value
            key_value_pairs.append(
                {
                    "field_value": document.text[
                        entity.text_anchor.text_segments[
                            0
                        ].start_index : entity.text_anchor.text_segments[0].end_index
                    ]
                    if entity.text_anchor.text_segments
                    else entity.mention_text,
                    "field_name": entity.type,  # Fallback if no specific field name is parsed
                }
            )

    return DocumentOutput(text=document.text, key_value_pairs=key_value_pairs)
