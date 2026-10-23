from document_client import get_textract_client
from document_models import KeyValueResponse, normalize_key_values


def extract_key_values(*, bucket: str = None, key: str = None, bytes_data: bytes = None) -> KeyValueResponse:
    client = get_textract_client()
    if bytes_data is not None:
        response = client.analyze_document(Document={"Bytes": bytes_data}, FeatureTypes=["FORMS"])
    else:
        if not bucket or not key:
            raise ValueError("bucket and key are required when bytes_data is not provided")
        response = client.analyze_document(Document={"S3Object": {"Bucket": bucket, "Name": key}}, FeatureTypes=["FORMS"])
    return KeyValueResponse(raw=response, key_values=normalize_key_values(response))
