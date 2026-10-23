import os
from google.cloud import vision_v1
from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions


GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

VISION_API_ENDPOINT = "vision.googleapis.com"
DOCUMENT_AI_ENDPOINT = "us-documentai.googleapis.com"

DOCUMENT_AI_PROCESSOR_ID = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "")
DOCUMENT_AI_LOCATION = os.environ.get("DOCUMENT_AI_LOCATION", "us")


def get_vision_client():
    client_options = ClientOptions(api_endpoint=VISION_API_ENDPOINT)
    return vision_v1.ImageAnnotatorClient(client_options=client_options)


def get_document_ai_client():
    client_options = ClientOptions(api_endpoint=DOCUMENT_AI_ENDPOINT)
    return documentai_v1.DocumentProcessorServiceClient(client_options=client_options)


def get_document_ai_processor_path():
    return documentai_v1.DocumentProcessorServiceClient.processor_path(
        project=GOOGLE_CLOUD_PROJECT_ID,
        location=DOCUMENT_AI_LOCATION,
        processor=DOCUMENT_AI_PROCESSOR_ID,
    )


def build_image_request(image_bytes, mime_type="image/png", feature_types=None):
    if feature_types is None:
        feature_types = [
            vision_v1.Feature.Type.TEXT_DETECTION,
            vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION,
            vision_v1.Feature.Type.IMAGE_PROPERTIES,
        ]
    image = vision_v1.Image(content=image_bytes)
    features = [vision_v1.Feature(type_=ft) for ft in feature_types]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    return request


def build_document_ai_process_request(image_bytes, mime_type="application/pdf"):
    import base64

    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    inline_document = documentai_v1.InlineDocument(
        content=encoded_content, mime_type=mime_type
    )
    raw_document = documentai_v1.RawDocument(
        content=inline_document.content, mime_type=inline_document.mime_type
    )
    request = documentai_v1.ProcessRequest(
        name=get_document_ai_processor_path(),
        raw_document=raw_document,
    )
    return request


def normalize_vision_text_response(response):
    texts = []
    for result in response.responses:
        if result.full_text_annotation:
            texts.append(result.full_text_annotation.text)
        elif result.text_annotations:
            if result.text_annotations:
                texts.append(result.text_annotations[0].description)
    return "\n".join(filter(None, texts))


def normalize_vision_layout_response(response):
    blocks = []
    for result in response.responses:
        if result.full_text_annotation:
            for page in result.full_text_annotation.pages:
                for block in page.blocks:
                    block_text = "".join(
                        symbol.text
                        for paragraph in block.paragraphs
                        for word in paragraph.words
                        for symbol in word.symbols
                    )
                    vertices = block.bounding_box.vertices
                    blocks.append(
                        {
                            "text": block_text.strip(),
                            "block_type": block.block_type,
                            "confidence": block.confidence,
                            "bounding_box": [{"x": v.x, "y": v.y} for v in vertices],
                        }
                    )
    return blocks


def normalize_document_ai_response(document):
    entities = []
    for entity in document.entities:
        entities.append(
            {
                "type": entity.type_,
                "mention_text": entity.mention_text,
                "confidence": entity.confidence,
            }
        )
    return entities


def normalize_document_ai_tables(document):
    tables = []
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
            tables.append(table_data)
    return tables


def normalize_document_ai_key_values(document):
    key_values = []
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
    return key_values
