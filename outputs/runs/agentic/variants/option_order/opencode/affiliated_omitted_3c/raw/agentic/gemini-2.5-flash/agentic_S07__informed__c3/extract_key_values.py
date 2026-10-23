from document_client import get_document_intelligence_client
from document_models import ExtractedKeyValuePair, BoundingBox
from azure.ai.documentintelligence.models import DocumentAnalysisFeature


def extract_key_values_from_document(document_path: str) -> list[ExtractedKeyValuePair]:
    client = get_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    extracted_key_values = []
    for doc in result.documents:
        for name, field in doc.fields.items():
            if (
                field.value_type == "string"
                and field.content
                and field.bounding_regions
                and field.key_bounding_regions
            ):
                key_bounding_box_data = field.key_bounding_regions[0].bounding_box
                value_bounding_box_data = field.bounding_regions[0].bounding_box

                extracted_key_values.append(
                    ExtractedKeyValuePair(
                        key=field.key_content if field.key_content else name,
                        value=field.content,
                        key_bounding_box=BoundingBox(
                            x1=key_bounding_box_data[0].x,
                            y1=key_bounding_box_data[0].y,
                            x2=key_bounding_box_data[2].x,
                            y2=key_bounding_box_data[2].y,
                        ),
                        value_bounding_box=BoundingBox(
                            x1=value_bounding_box_data[0].x,
                            y1=value_bounding_box_data[0].y,
                            x2=value_bounding_box_data[2].x,
                            y2=value_bounding_box_data[2].y,
                        ),
                    )
                )

    return extracted_key_values
