from google.cloud import vision

from storage_client import get_bucket
from storage_models import normalize_object_name


def stored_document_ocr(bucket: str, object_name: str):
    client = vision.ImageAnnotatorClient()
    blob = get_bucket(bucket).blob(normalize_object_name(object_name))
    gcs_source = vision.GcsSource(uri=f"gs://{bucket}/{blob.name}")
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type="application/pdf")
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    request = vision.AsyncAnnotateFileRequest(features=[feature], input_config=input_config, output_config=vision.OutputConfig(gcs_destination=vision.GcsDestination(uri=f"gs://{bucket}/ocr-output/"), batch_size=1))
    operation = client.async_batch_annotate_files(requests=[request])
    operation.result()
    return f"gs://{bucket}/ocr-output/"
