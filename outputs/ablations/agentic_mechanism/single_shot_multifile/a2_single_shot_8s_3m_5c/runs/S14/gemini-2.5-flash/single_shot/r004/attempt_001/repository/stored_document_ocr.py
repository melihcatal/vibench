import os
from google.cloud import vision
from presigned_download import create_presigned_download_url
from storage_client import get_s3_bucket_name

def run_ocr_on_stored_document(
    object_key: str,
    bucket_name: Optional[str] = None
) -> dict:
    if bucket_name is None:
        bucket_name = get_s3_bucket_name()

    presigned_url_response = create_presigned_download_url(
        bucket_name=bucket_name,
        object_key=object_key,
        expiration=3600
    )

    if presigned_url_response["status"] != "success":
        return {"status": "error", "message": f"Failed to generate presigned URL: {presigned_url_response['message']}"}
    
    image_uri = presigned_url_response["url"]

    client = vision.ImageAnnotatorClient()
    image = vision.Image(source=vision.ImageSource(image_uri=image_uri))

    try:
        response = client.document_text_detection(image=image)
        full_text_annotation = response.full_text_annotation

        detected_languages = []
        if full_text_annotation and full_text_annotation.pages:
            for page in full_text_annotation.pages:
                for block in page.blocks:
                    if block.property and block.property.detected_languages:
                        for lang in block.property.detected_languages:
                            if lang.language_code not in detected_languages:
                                detected_languages.append(lang.language_code)

        return {
            "status": "success",
            "object_key": object_key,
            "extracted_text": full_text_annotation.text if full_text_annotation else "",
            "detected_languages": detected_languages
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
