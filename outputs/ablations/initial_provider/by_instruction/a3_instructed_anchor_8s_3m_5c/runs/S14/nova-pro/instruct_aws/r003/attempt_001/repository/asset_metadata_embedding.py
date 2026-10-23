import boto3
import io
from PIL import Image
import pytesseract
import embed

def asset_metadata_embedding(bucket_name, object_key, metadata):
    text = stored_document_ocr(bucket_name, object_key)
    embedding = embed.embed_text(text, metadata)
    return embedding