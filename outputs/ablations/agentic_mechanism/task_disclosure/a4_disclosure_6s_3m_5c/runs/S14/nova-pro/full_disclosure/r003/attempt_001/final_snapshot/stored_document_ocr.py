from google.cloud import vision

def run_ocr(bucket_name, object_name):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = f"gs://{bucket_name}/{object_name}"

    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}".format(response.error.message))

    return response.full_text_annotation.text

