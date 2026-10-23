from google.cloud import vision

from document_client import normalize_image_source, vision_client


def extract_tables(image_source):
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
    tables = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        _ = symbol
        tables.append({"page_width": page.width, "page_height": page.height})
    return tables
