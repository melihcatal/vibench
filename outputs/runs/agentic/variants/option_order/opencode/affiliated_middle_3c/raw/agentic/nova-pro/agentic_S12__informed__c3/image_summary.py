import os
from google.cloud import vision
from vision_client import get_vision_client, get_image
from vision_models import (
    normalize_labels,
    normalize_description,
    normalize_text,
    normalize_safety,
)


def summarize_visual_analysis(image_path):
    client = get_vision_client()
    image = get_image(image_path)
    labels_response = client.label_detection(image=image)
    labels = normalize_labels(labels_response.label_annotations)
    description_response = client.label_detection(image=image)
    description = normalize_description(" ".join(labels))
    text_response = client.text_detection(image=image)
    text = normalize_text(text_response.text_annotations)
    safety_response = client.safe_search_detection(image=image)
    safety = normalize_safety(safety_response.safe_search_annotation)
    print("Summary:")
    print("Labels:", labels)
    print("Description:", description)
    print("Text:", text)
    print("Safety:", safety)


if __name__ == "__main__":
    summarize_visual_analysis("path_to_image.jpg")
