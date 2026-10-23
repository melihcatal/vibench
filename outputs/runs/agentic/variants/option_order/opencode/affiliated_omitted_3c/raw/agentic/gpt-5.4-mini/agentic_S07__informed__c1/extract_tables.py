from document_client import get_textract_client
from document_models import TableResponse, normalize_tables


def extract_tables(*, bucket: str = None, key: str = None, bytes_data: bytes = None) -> TableResponse:
    client = get_textract_client()
    if bytes_data is not None:
        response = client.analyze_document(Document={"Bytes": bytes_data}, FeatureTypes=["TABLES"])
    else:
        if not bucket or not key:
            raise ValueError("bucket and key are required when bytes_data is not provided")
        response = client.analyze_document(Document={"S3Object": {"Bucket": bucket, "Name": key}}, FeatureTypes=["TABLES"])
    return TableResponse(raw=response, tables=normalize_tables(response))
