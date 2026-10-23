import boto3
import io
from PIL import Image
import pytesseract
import summarize

def stored_asset_summary(bucket_name, object_key):
    text = stored_document_ocr(bucket_name, object_key)
    summary = summarize.summarize_text(text)
    return summary