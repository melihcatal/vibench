from google.cloud import vision_v1p4beta1 as vision
from google.cloud import storage
from storage_models import ObjectMetadataRequest # Reusing for simplicity to identify the document
from dataclasses import dataclass
from typing import Optional

@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    blob_name: str

@dataclass
class StoredDocumentOcrResponse:
    text: str
    full_response: Optional[dict] = None

def run_ocr_on_stored_document(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    client = vision.ImageAnnotatorClient()
    
    # Construct the GCS URI for the image
    gcs_source_uri = f"gs://{request.bucket_name}/{request.blob_name}"
    source = {'image_uri': gcs_source_uri}
    image = vision.Image(source=source)

    # Set the feature type to DOCUMENT_TEXT_DETECTION for comprehensive OCR
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    # Perform the OCR request
    response = client.annotate_image({'image': image, 'features': [feature]})
    
    full_text_annotation = response.full_text_annotation
    text = full_text_annotation.text if full_text_annotation else ""

    return StoredDocumentOcrResponse(text=text, full_response=vision.AnnotateImageResponse.to_dict(response))
