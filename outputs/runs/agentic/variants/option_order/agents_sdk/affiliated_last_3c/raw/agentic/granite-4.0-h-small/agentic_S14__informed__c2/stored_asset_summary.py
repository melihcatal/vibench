import os
from storage_models import normalize_object_info
from stored_document_ocr import stored_document_ocr
from stored_text_translate import stored_text_translate
from typing import Dict, Any

def stored_asset_summary(bucket: str, key: str, language: str = 'fr'):
    """Generate a brief summary of a stored asset (document, image, etc.).

    1. Extract text via OCR if the asset is a PDF/image.
    2. Translate the extracted text to the requested language.
    3. Produce a concise English summary (simulated with a placeholder).

    bucket: S3 bucket name
    key: object key/path to the stored asset
    language: target language for translation (default 'fr')
    Returns a dict containing original language, translated text, and summary.
    """
    # a) Detect if OCR needed - simple heuristic: file extension
    import mimetypes
    mime_type, _ = mimetypes.guess_type(key)
    needs_ocr = mime_type in (None, 'application/pdf', 'image/', 'application/octet-stream')

    # b) If OCR needed, use OCR step
    if needs_ocr:
        extracted_text = stored_document_ocr(bucket, key)
    else:
        # Assume plaintext or JSON - fetch directly
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        obj = s3.get_object(Bucket=bucket, Key=key)
        extracted_text = obj['Body'].read().decode('utf-8')

    # c) Translate the extracted text
    translated_text = stored_text_translate(bucket, key, target_lang=language)

    # d) Simulate a summary (replace with LLM call in production)
    summary = f"Summary of {key}: {extracted_text[:200]}..."

    return {
        'bucket': bucket,
        'key': key,
        'original_text_preview': extracted_text[:300],
        'translated_text': translated_text[:300],
        'summary': summary
    }
