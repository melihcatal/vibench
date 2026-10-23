from google.cloud import vision
import base64
from typing import List, Dict, Any

def create_image_from_bytes(image_content: bytes) -> vision.Image:
    return vision.Image(content=image_content)

def create_image_from_gcs_uri(gcs_uri: str) -> vision.Image:
    return vision.Image(source=vision.ImageSource(gcs_image_uri=gcs_uri))

def create_feature(feature_type: vision.Feature.Type, max_results: int = 10) -> vision.Feature:
    return vision.Feature(type=feature_type, max_results=max_results)

def parse_label_annotations(response: vision.AnnotateImageResponse) -> List[Dict[str, Any]]:
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append({
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality,
            })
    return labels
