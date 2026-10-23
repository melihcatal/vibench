import json

from storage_client import (
    get_s3_client,
    get_textract_client,
    validate_bucket_name,
    handle_s3_error,
)
from storage_models import OcrRequest, OcrResponse, normalize_ocr_response


def run_ocr_on_stored_document(
    bucket: str,
    key: str,
    feature_types: list = None,
    region_name: str = None,
) -> OcrResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    textract = get_textract_client(region_name=region_name)
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        document_bytes = obj["Body"].read()
    except Exception as exc:
        handle_s3_error(exc, "get_object", bucket, key)
    features = feature_types or ["TABLES", "FORMS"]
    try:
        response = textract.analyze_document(
            Document={"Bytes": document_bytes},
            FeatureTypes=features,
        )
        return normalize_ocr_response(response, bucket, key)
    except Exception as exc:
        error_code = (
            exc.response.get("Error", {}).get("Code", "Unknown")
            if hasattr(exc, "response")
            else "Unknown"
        )
        error_message = (
            exc.response.get("Error", {}).get("Message", str(exc))
            if hasattr(exc, "response")
            else str(exc)
        )
        raise RuntimeError(
            f"AWS Textract analyze_document failed [{error_code}]: {error_message} "
            f"(Bucket: {bucket}, Key: {key})"
        ) from exc


def run_ocr_from_request(
    request: OcrRequest,
    region_name: str = None,
) -> OcrResponse:
    return run_ocr_on_stored_document(
        bucket=request.bucket,
        key=request.key,
        feature_types=request.feature_types,
        region_name=region_name,
    )


def run_ocr_on_s3_object(
    bucket: str,
    key: str,
    region_name: str = None,
) -> OcrResponse:
    return run_ocr_on_stored_document(
        bucket=bucket,
        key=key,
        feature_types=["TABLES", "FORMS"],
        region_name=region_name,
    )
