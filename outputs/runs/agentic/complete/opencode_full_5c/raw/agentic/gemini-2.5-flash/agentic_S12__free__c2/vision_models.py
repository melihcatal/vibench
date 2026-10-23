import json


def construct_image_source(image_uri=None, image_content=None):
    if image_uri:
        return {"image_uri": image_uri}
    elif image_content:
        return {"content": image_content}
    return {}


def parse_label_detection_response(response):
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append(label.description)
    return {"labels": labels}


def parse_text_detection_response(response):
    texts = []
    if response.text_annotations:
        for text in response.text_annotations:
            texts.append(text.description)
    return {"texts": texts}


def parse_safe_search_detection_response(response):
    safe_search_annotation = response.safe_search_annotation
    if safe_search_annotation:
        return {
            "adult": safe_search_annotation.adult,
            "racy": safe_search_annotation.racy,
            "medical": safe_search_annotation.medical,
            "violence": safe_search_annotation.violence,
            "spoof": safe_search_annotation.spoof,
        }
    return {}
