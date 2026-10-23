import boto3
from storage_client import get_s3_client, get_textract_client
from storage_models import TextractResponse


def stored_document_ocr(bucket_name, object_key):
    s3_client = get_s3_client()
    textract_client = get_textract_client()
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_bytes = response["Body"].read()
    textract_response = textract_client.detect_document_text(
        Document={"Bytes": image_bytes}
    )
    text = "".join(
        [
            line["Text"]
            for block in textract_response["Blocks"]
            if block["BlockType"] == "LINE"
            for line in block["Geometry"]["Polygon"]
        ]
    )
    return TextractResponse(text)
