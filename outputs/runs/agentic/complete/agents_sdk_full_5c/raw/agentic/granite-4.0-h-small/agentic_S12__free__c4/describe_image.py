# describe_image.py
import json
import uuid
from google.cloud import vision_v1
from vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient()
    image = client.get_image(image_path)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.IMAGE_PROPERTIES),
                vision_v1.Feature(type_=vision_v1.Feature.Type.OBJECT_LOCALIZATION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.service.annotate_image(request)
    # Simple short description based on dominant objects and colors
    objects = [ann.description for ann in response.object_annotations]
    dominant_colors = response.image_properties_annotation.dominant_colors.colors
    colors = [f"#{int(c.pixel_rgb.red):02x}{int(c.pixel_rgb.green):02x}{int(c.pixel_rgb.blue):02x}" for c in dominant_colors]
    description = f"Image contains {', '.join(objects)} with dominant colors {', '.join(colors)}."
    return description[:100]  # truncate to a short snippet
