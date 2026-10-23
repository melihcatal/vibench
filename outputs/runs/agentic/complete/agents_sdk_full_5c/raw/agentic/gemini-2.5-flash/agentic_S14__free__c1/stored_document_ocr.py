import os
import json
from storage_client import StorageClient
from storage_models import DocumentText

def run_ocr_on_s3_document(bucket_name: str, object_name: str) -> DocumentText:
    """
    Runs OCR using AWS Textract on a document stored in S3.
    Assumes the document is suitable for synchronous Textract processing (e.g., PDF, JPG, PNG).
    For larger documents or asynchronous processing, start_document_text_detection/start_document_analysis would be used.
    """
    storage_client = StorageClient()
    textract_client = storage_client.get_textract_client()

    try:
        response = textract_client.detect_document_text(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': object_name}}
        )

        detected_text = []
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                detected_text.append(item['Text'])
        
        full_text = "\n".join(detected_text)
        return DocumentText(text=full_text, source_language=None) # Textract does not provide source language directly

    except textract_client.exceptions.InvalidS3ObjectException as e:
        print(f"Invalid S3 object or permissions issue: {e}")
        return DocumentText(text="", source_language=None)
    except textract_client.exceptions.BadDocumentException as e:
        print(f"Bad document format or content for Textract: {e}")
        return DocumentText(text="", source_language=None)
    except Exception as e:
        print(f"Error running OCR with AWS Textract: {e}")
        return DocumentText(text="", source_language=None)

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # For testing, you would need an actual document in S3.
    # BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    # DOCUMENT_KEY = "path/to/your/document.pdf" # or .png, .jpg
    #
    # ocr_result = run_ocr_on_s3_document(BUCKET, DOCUMENT_KEY)
    # if ocr_result.text:
    #     print("OCR Extracted Text:")
    #     print(ocr_result.text[:500] + "..." if len(ocr_result.text) > 500 else ocr_result.text)
    # else:
    #     print("Failed to extract text via OCR.")
    pass
