from document_client import DocumentClient
from document_models import ExtractedLayout

def extract_layout(payload, config=None):
    client = DocumentClient(region_name=config.get("region")).get_textract_client()
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["LAYOUT"]
    )
    return ExtractedLayout(blocks=response["Blocks"])
