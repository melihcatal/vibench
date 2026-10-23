from typing import List, Optional, Dict
from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions
from document_client import (
    get_document_ai_client,
    get_document_ai_processor_path,
    normalize_document_ai_key_values,
    GOOGLE_CLOUD_PROJECT_ID,
    DOCUMENT_AI_LOCATION,
)
from document_models import (
    KeyValueRequest,
    KeyValueResponse,
    KeyValuePair,
    BoundingBox,
    normalize_kv_response,
)


DOCUMENT_AI_ENDPOINT = "us-documentai.googleapis.com"
GOOGLE_DOCUMENT_AI_FORM_PARSER_MODEL = "builtin/latest"


def extract_key_values_from_image(
    image_bytes: bytes,
    mime_type: str = "image/png",
    form_type: Optional[str] = None,
) -> KeyValueResponse:
    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    import base64

    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    raw_document = documentai_v1.RawDocument(
        content=encoded_content, mime_type=mime_type
    )
    process_request = documentai_v1.ProcessRequest(
        name=processor_path, raw_document=raw_document
    )
    response = client.process_document(request=process_request)
    document = response.document
    kv_data = []
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
                kv_data.append(
                    {
                        "key": key_text,
                        "value": value_text,
                        "confidence": entity.confidence,
                    }
                )
    return normalize_kv_response(kv_data)


def extract_key_values_from_gcs_uri(
    gcs_uri: str,
    mime_type: str = "application/pdf",
    form_type: Optional[str] = None,
) -> KeyValueResponse:
    client = get_document_ai_client()
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
    operation = client.batch_process_documents(request=request)
    operation.result()
    return KeyValueResponse(pairs=[])


def extract_form_fields_with_confidence(
    image_bytes: bytes,
    mime_type: str = "image/png",
    min_confidence: float = 0.5,
) -> List[Dict[str, str]]:
    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    import base64

    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    raw_document = documentai_v1.RawDocument(
        content=encoded_content, mime_type=mime_type
    )
    process_request = documentai_v1.ProcessRequest(
        name=processor_path, raw_document=raw_document
    )
    response = client.process_document(request=process_request)
    document = response.document
    form_fields = []
    for entity in document.entities:
        if entity.type_ == "KEY_VALUE_SET" and entity.confidence >= min_confidence:
            key_text = ""
            value_text = ""
            for prop in entity.properties:
                if prop.type_ == "key":
                    key_text = prop.mention_text
                elif prop.type_ == "value":
                    value_text = prop.mention_text
            if key_text and value_text:
                form_fields.append(
                    {
                        "field_name": key_text,
                        "field_value": value_text,
                        "confidence": str(entity.confidence),
                    }
                )
    return form_fields
