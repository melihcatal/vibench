from google.cloud import vision

from document_client import normalize_image_source, vision_client


def extract_layout(image_source):
    client = vision_client()
    src = normalize_image_source(image_source)
    if "content" in src:
        image = vision.Image(content=src["content"])
    elif "uri" in src:
        image = vision.Image(source=vision.ImageSource(image_uri=src["uri"]))
    else:
        with open(src["path"], "rb") as f:
            image = vision.Image(content=f.read())
    response = client.document_text_detection(image=image)
    doc = response.full_text_annotation
    return {"pages": [page._pb for page in doc.pages], "text": doc.text}
