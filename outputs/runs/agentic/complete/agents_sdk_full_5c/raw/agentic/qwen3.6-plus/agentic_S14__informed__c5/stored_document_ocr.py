"""
stored_document_ocr.py - Run OCR on a stored document object.

Uses Google Document AI via google-cloud-documentai as the concrete OCR provider.
Authentication via GOOGLE_APPLICATION_CREDENTIALS environment variable.
"""

import os
from typing import Optional, List
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import Document


def run_ocr_on_stored_document(
    gcp_project_id: str,
    gcp_location: str,
    processor_id: str,
    document_mime_type: str,
    document_content: bytes,
    credential_path: Optional[str] = None,
) -> Document:
    """
    Run OCR on a stored document using Google Document AI.

    Processes the document content and extracts text, layout, and structural
    information using Google's Document AI processor.

    Args:
        gcp_project_id: Google Cloud project ID.
        gcp_location: GCP location (e.g., 'us', 'eu').
        processor_id: Document AI processor ID.
        document_mime_type: MIME type of the document (e.g., 'application/pdf', 'image/png').
        document_content: Raw bytes of the document to process.
        credential_path: Optional path to Google service account JSON credentials.

    Returns:
        Google Document AI Document response with OCR results.

    Raises:
        ValueError: If required parameters are missing.
        RuntimeError: If OCR processing fails.
    """
    if not gcp_project_id or not gcp_location or not processor_id:
        raise ValueError("gcp_project_id, gcp_location, and processor_id are required.")

    if not document_content:
        raise ValueError("document_content bytes are required.")

    if credential_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

    client_options = {
        "api_endpoint": f"{gcp_location}-documentai.googleapis.com"
    }

    client = documentai.DocumentProcessorServiceClient(
        client_options=client_options
    )

    name = client.processor_path(gcp_project_id, gcp_location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_content,
        mime_type=document_mime_type,
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
    )

    try:
        result = client.process_document(request=request)
        return result.document

    except Exception as e:
        raise RuntimeError(
            f"Google Document AI OCR processing failed: {e}"
        ) from e


def extract_text_from_ocr_result(document: Document) -> str:
    """
    Extract full text content from a Google Document AI OCR response.

    Args:
        document: Document AI Document response.

    Returns:
        Extracted text string from the document.
    """
    return document.text


def extract_pages_from_ocr_result(document: Document) -> List[dict]:
    """
    Extract per-page text and bounding box information from OCR results.

    Args:
        document: Document AI Document response.

    Returns:
        List of dicts with page_number, text, and bounding_box data.
    """
    pages = []
    text = document.text

    for page in document.pages:
        page_text_segments = []
        for paragraph in page.paragraphs:
            segment = text[
                paragraph.layout.text_anchor.text_segments[0].start_index :
                paragraph.layout.text_anchor.text_segments[-1].end_index
            ]
            bounding_box = {
                "vertices": [
                    {"x": v.x, "y": v.y}
                    for v in paragraph.layout.bounding_poly.normalized_vertices
                ]
            }
            page_text_segments.append({
                "text": segment,
                "bounding_box": bounding_box,
            })

        pages.append({
            "page_number": page.page_number,
            "segments": page_text_segments,
        })

    return pages


def run_ocr_on_s3_object(
    gcp_project_id: str,
    gcp_location: str,
    processor_id: str,
    s3_bucket: str,
    s3_key: str,
    document_mime_type: str = "application/pdf",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: Optional[str] = None,
    gcp_credential_path: Optional[str] = None,
) -> Document:
    """
    Download an object from Amazon S3 and run OCR on it using Google Document AI.

    Args:
        gcp_project_id: Google Cloud project ID.
        gcp_location: GCP location for Document AI.
        processor_id: Document AI processor ID.
        s3_bucket: S3 bucket containing the document.
        s3_key: S3 object key of the document.
        document_mime_type: MIME type of the document.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        aws_region: Optional AWS region.
        gcp_credential_path: Optional GCP credentials path.

    Returns:
        Document AI Document response with OCR results.
    """
    import boto3

    s3_session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region or "us-east-1",
    )
    s3_client = s3_session.client("s3")

    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    document_content = response["Body"].read()

    return run_ocr_on_stored_document(
        gcp_project_id=gcp_project_id,
        gcp_location=gcp_location,
        processor_id=processor_id,
        document_mime_type=document_mime_type,
        document_content=document_content,
        credential_path=gcp_credential_path,
    )
