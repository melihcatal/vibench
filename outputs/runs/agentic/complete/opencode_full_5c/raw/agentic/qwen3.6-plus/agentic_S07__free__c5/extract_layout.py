from typing import List, Optional
from google.cloud import vision_v1
from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions
from document_client import (
    get_vision_client,
    get_document_ai_client,
    get_document_ai_processor_path,
    GOOGLE_CLOUD_PROJECT_ID,
    DOCUMENT_AI_LOCATION,
    normalize_vision_layout_response,
    normalize_document_ai_response,
)
from document_models import (
    LayoutRequest,
    LayoutResponse,
    LayoutBlock,
    BoundingBox,
    normalize_layout_response,
)


VISION_API_ENDPOINT = "vision.googleapis.com"
DOCUMENT_AI_ENDPOINT = "us-documentai.googleapis.com"
GOOGLE_DOCUMENT_AI_MODEL = "builtin/latest"


def extract_layout_from_image(
    image_bytes: bytes,
    mime_type: str = "image/png",
    include_tables: bool = True,
    include_forms: bool = True,
) -> LayoutResponse:
    client = get_vision_client()
    image = vision_v1.Image(content=image_bytes)
    features = [
        vision_v1.Feature(type_=vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION),
        vision_v1.Feature(type_=vision_v1.Feature.Type.TEXT_DETECTION),
    ]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request=request)
    blocks_data = normalize_vision_layout_response(response)
    layout_response = normalize_layout_response(blocks_data)
    tables_data = []
    key_values = []
    if include_tables or include_forms:
        doc_ai_client = get_document_ai_client()
        processor_path = get_document_ai_processor_path()
        import base64

        encoded_content = base64.b64encode(image_bytes).decode("utf-8")
        raw_document = documentai_v1.RawDocument(
            content=encoded_content, mime_type=mime_type
        )
        process_request = documentai_v1.ProcessRequest(
            name=processor_path, raw_document=raw_document
        )
        doc_ai_response = doc_ai_client.process_document(request=process_request)
        document = doc_ai_response.document
        if include_tables:
            for page in document.pages:
                for table in page.tables:
                    table_data = []
                    for row in table.table_rows:
                        row_data = []
                        for cell in row.cells:
                            cell_text = ""
                            if cell.layout and cell.layout.text_anchor:
                                for segment in cell.layout.text_anchor.text_segments:
                                    cell_text += document.text[
                                        segment.start_index : segment.end_index
                                    ]
                            row_data.append(
                                {
                                    "text": cell_text.strip(),
                                    "row_span": cell.row_span,
                                    "col_span": cell.col_span,
                                    "confidence": cell.confidence,
                                }
                            )
                        table_data.append(row_data)
                    tables_data.append(table_data)
        if include_forms:
            for entity in document.entities:
                if entity.type_ == "KEY_VALUE_SET":
                    key_text = ""
                    value_text = ""
                    for prop in entity.properties:
                        if prop.type_ == "key":
                            key_text = prop.mention_text
                        elif prop.type_ == "value":
                            value_text = prop.mention_text
                    if key_text and value_text:
                        key_values.append(
                            {
                                "key": key_text,
                                "value": value_text,
                                "confidence": entity.confidence,
                            }
                        )
    layout_response.tables = tables_data
    layout_response.key_values = key_values
    return layout_response


def extract_layout_from_gcs_uri(
    gcs_uri: str,
    mime_type: str = "application/pdf",
    include_tables: bool = True,
    include_forms: bool = True,
) -> LayoutResponse:
    doc_ai_client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    gcs_document = documentai_v1.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    gcs_documents = documentai_v1.GcsDocuments(documents=[gcs_document])
    input_config = documentai_v1.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
    output_config = documentai_v1.OutputConfig(
        gcs_destination=documentai_v1.GcsDestination(uri="gs://temp-output-bucket/")
    )
    request = documentai_v1.BatchProcessRequest(
        name=processor_path,
        input_documents=input_config,
        document_output_config=output_config,
    )
    operation = doc_ai_client.batch_process_documents(request=request)
    operation.result()
    metadata = operation.metadata
    process_responses = []
    for process in metadata.individual_process_statuses:
        if process.output_gcs_destination:
            pass
    return LayoutResponse(blocks=[])
